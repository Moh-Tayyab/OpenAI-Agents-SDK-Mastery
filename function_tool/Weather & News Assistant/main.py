from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio
import os
from dotenv import load_dotenv
from location_tool import get_user_location
from weather_tool import get_weather_by_location
from new_tool import get_latest_news
load_dotenv()


async def main():
    MODEL_NAME = "gemini-2.0-flash"
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("Gemini Api key not found.")
    client = AsyncOpenAI(
        api_key=API_KEY, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
    #API_KEY = os.getenv("OPENAI_API_KEY")
    #if not API_KEY:
        #raise ValueError("OpenAI Api key not found.")
        
    agent = Agent(
        name="WeatherNewsAgent",
        instructions="""You are a professional weather and news assistant. Your role is to provide comprehensive, real-time information to users.

IMPORTANT GUIDELINES:
1. LOCATION PRIORITY: When users specify a location (like "Lahore weather" or "weather in London"), use that exact location - DO NOT use get_user_location()
2. AUTO-DETECTION: Only use get_user_location() when users don't specify any location (like "what's the weather like?" or "show me news")
3. For weather requests: Use get_weather_by_location() with the user's specified location or detected location
4. For news requests: Use get_latest_news() with the user's specified location or detected location
5. Be proactive - if a user asks about weather or news without specifying location, automatically detect their location
6. Provide professional, friendly responses with complete information
7. Format responses clearly with proper structure and details
8. If any tool fails, provide helpful error messages and suggest alternatives

RESPONSE FORMAT:
- Weather: Include location, temperature, conditions, humidity, wind speed, and any relevant weather alerts
- News: Include location context and provide 3-5 latest headlines with brief context
- Always be helpful and informative

EXAMPLES:
- User asks "Lahore weather" → Use get_weather_by_location("Lahore")
- User asks "weather in London" → Use get_weather_by_location("London")  
- User asks "what's the weather like?" → Use get_user_location() then get_weather_by_location()
- User asks "Lahore news" → Use get_latest_news("Lahore")
- User asks "show me news" → Use get_user_location() then get_latest_news()""",
        model = model,
        tools = [get_user_location, get_weather_by_location, get_latest_news]
    )
    query = input("How can I assist you with weather or news updates? ")
    
    result = await Runner.run(
        starting_agent=agent,
        input=query
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())