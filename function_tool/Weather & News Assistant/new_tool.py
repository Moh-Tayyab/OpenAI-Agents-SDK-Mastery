from agents import function_tool
from dotenv import load_dotenv
import os
import requests

load_dotenv()

NEW_API_KEY = os.getenv("NEW_API_KEY")

@function_tool
def get_latest_news(location: str, topic: str = "general") -> list[str]:
    """
    Fetch the latest news headlines for a specific topic and location.

    Args:
        location (str): The location (e.g., country or city) for news.
        topic (str, optional): The topic/category of news. Defaults to "general".

    Returns:
        list[str]: A list of news headlines.
    """
    if not NEW_API_KEY:
        raise ValueError("News API key is not set.")

    # Use GNews API for fetching news - prefer search for more diverse results
    url = "https://gnews.io/api/v4/search"
    
    # Map common location names to country codes for better results
    country_mapping = {
        "pakistan": "pk", "karachi": "pk", "lahore": "pk", "islamabad": "pk",
        "united states": "us", "usa": "us", "new york": "us", "los angeles": "us",
        "united kingdom": "gb", "uk": "gb", "london": "gb",
        "canada": "ca", "toronto": "ca", "vancouver": "ca",
        "australia": "au", "sydney": "au", "melbourne": "au",
        "india": "in", "mumbai": "in", "delhi": "in"
    }
    
    # Try to find country code from location
    country_code = None
    location_lower = location.lower()
    for key, code in country_mapping.items():
        if key in location_lower:
            country_code = code
            break
    
    # Build search query based on topic and location
    if topic.lower() in ["general", "news", "latest"]:
        if country_code:
            # For general news, use country-specific search
            search_query = f"latest news {location}"
        else:
            search_query = f"latest news {location}"
    else:
        # For specific topics, include both topic and location
        search_query = f"{topic} {location}"
    
    params = {
        "token": NEW_API_KEY,
        "lang": "en",
        "max": 10,
        "sortby": "publishedAt",
        "q": search_query
    }
    
    # Add country filter if available
    if country_code:
        params["country"] = country_code
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("articles"):
            news_items = []
            seen_titles = set()  # To avoid duplicate headlines
            
            for article in data["articles"]:
                if len(news_items) >= 5:  # Limit to 5 articles
                    break
                    
                title = article.get("title", "No title")
                
                # Skip if we've already seen this title
                if title in seen_titles:
                    continue
                    
                source = article.get("source", {}).get("name", "Unknown source")
                published_at = article.get("publishedAt", "")
                
                # Format the date if available
                if published_at:
                    try:
                        from datetime import datetime
                        date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        date_str = date_obj.strftime("%b %d, %H:%M")
                    except:
                        date_str = ""
                else:
                    date_str = ""
                
                # Create news item with date
                if date_str:
                    news_items.append(f"📰 {title} (Source: {source} • {date_str})")
                else:
                    news_items.append(f"📰 {title} (Source: {source})")
                
                seen_titles.add(title)
            
            if news_items:
                return news_items
            else:
                return ["No fresh news articles found for the specified topic and location."]
        else:
            return ["No news articles found for the specified topic and location."]
    except requests.RequestException as e:
        return [f"Error fetching news: {str(e)}"]