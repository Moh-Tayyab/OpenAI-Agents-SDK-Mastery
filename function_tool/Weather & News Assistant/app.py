import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from location_tool import get_user_location
from weather_tool import get_weather_by_location
from new_tool import get_latest_news
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Weather & News Assistant",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .news-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #a8e6cf 0%, #7fcdcd 100%);
        color: #2d3748;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'user_location' not in st.session_state:
    st.session_state.user_location = None

def initialize_agent():
    """Initialize the agent"""
    try:
        MODEL_NAME = "gemini-2.0-flash"
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            st.error("❌ Gemini API key not found. Please check your environment variables.")
            return None
            
        client = AsyncOpenAI(
            api_key=API_KEY, 
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        model = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
        
        agent = Agent(
            name="WeatherNewsAgent",
            instructions="""You are a professional weather and news assistant. Your role is to provide comprehensive, real-time information to users.

IMPORTANT GUIDELINES:
1. ALWAYS detect the user's location first using get_user_location() when they ask about weather or news
2. For weather requests: Use get_weather_by_location() and provide detailed information including temperature, conditions, humidity, and wind speed
3. For news requests: Use get_latest_news() and provide the latest headlines with context
4. Be proactive - if a user asks about weather or news without specifying location, automatically detect their location
5. Provide professional, friendly responses with complete information
6. Format responses clearly with proper structure and details
7. If any tool fails, provide helpful error messages and suggest alternatives

RESPONSE FORMAT:
- Weather: Include location, temperature, conditions, humidity, wind speed, and any relevant weather alerts
- News: Include location context and provide 3-5 latest headlines with brief context
- Always be helpful and informative""",
            model=model,
            tools=[get_user_location, get_weather_by_location, get_latest_news]
        )
        return agent
    except Exception as e:
        st.error(f"❌ Error initializing agent: {str(e)}")
        return None

async def get_agent_response(user_input):
    """Get response from the agent"""
    try:
        if st.session_state.agent:
            result = await Runner.run(
                starting_agent=st.session_state.agent,
                input=user_input
            )
            return result.final_output
        else:
            return "❌ Agent not initialized. Please check your API keys."
    except Exception as e:
        return f"❌ Error getting response: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🌤️ Weather & News Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered companion for real-time weather and news updates</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Initialize agent
        if st.button("🔄 Initialize Agent"):
            with st.spinner("Initializing agent..."):
                st.session_state.agent = initialize_agent()
                if st.session_state.agent:
                    st.success("✅ Agent initialized successfully!")
                else:
                    st.error("❌ Failed to initialize agent")
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("📍 Detect My Location"):
            if st.session_state.agent:
                with st.spinner("Detecting your location..."):
                    try:
                        location = get_user_location()
                        st.session_state.user_location = location
                        st.success(f"📍 Location detected: {location}")
                    except Exception as e:
                        st.error(f"❌ Error detecting location: {str(e)}")
            else:
                st.warning("⚠️ Please initialize the agent first")
        
        if st.button("🌤️ Get Weather"):
            if st.session_state.user_location and st.session_state.agent:
                with st.spinner("Fetching weather..."):
                    try:
                        weather = get_weather_by_location(st.session_state.user_location)
                        if "error" not in weather:
                            st.success("✅ Weather fetched successfully!")
                        else:
                            st.error(f"❌ Weather error: {weather['error']}")
                    except Exception as e:
                        st.error(f"❌ Error fetching weather: {str(e)}")
            else:
                st.warning("⚠️ Please detect your location first")
        
        if st.button("📰 Get Latest News"):
            if st.session_state.user_location and st.session_state.agent:
                with st.spinner("Fetching news..."):
                    try:
                        news = get_latest_news(st.session_state.user_location)
                        if news and "Error" not in news[0]:
                            st.success("✅ News fetched successfully!")
                        else:
                            st.error("❌ Error fetching news")
                    except Exception as e:
                        st.error(f"❌ Error fetching news: {str(e)}")
            else:
                st.warning("⚠️ Please detect your location first")
        
        # API Status
        st.markdown("### 🔧 API Status")
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.success("✅ Gemini API Key: Configured")
        else:
            st.error("❌ Gemini API Key: Missing")
        
        location_key = os.getenv("LOCATION_API_KEY")
        if location_key:
            st.success("✅ Location API Key: Configured")
        else:
            st.error("❌ Location API Key: Missing")
        
        weather_key = os.getenv("OPENWEATHER_API_KEY")
        if weather_key:
            st.success("✅ Weather API Key: Configured")
        else:
            st.error("❌ Weather API Key: Missing")
        
        news_key = os.getenv("NEW_API_KEY")
        if news_key:
            st.success("✅ News API Key: Configured")
        else:
            st.error("❌ News API Key: Missing")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Chat with Assistant")
        
        # Agent status
        if st.session_state.agent:
            st.success("✅ Agent is ready! You can start chatting.")
        else:
            st.warning("⚠️ Agent not initialized. Please click '🔄 Initialize Agent' in the sidebar.")
        
        # Chat interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask me about weather or news..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    if not st.session_state.agent:
                        response = "❌ Agent not initialized. Please click '🔄 Initialize Agent' in the sidebar first."
                    else:
                        response = asyncio.run(get_agent_response(prompt))
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.markdown("### 📍 Current Location")
        if st.session_state.user_location:
            st.info(f"📍 {st.session_state.user_location}")
        else:
            st.warning("📍 Location not detected")
        
        st.markdown("### 💡 Quick Tips")
        st.markdown("""
        - Ask: "What's the weather like?"
        - Ask: "Show me the latest news"
        - Ask: "What's the weather in [city]?"
        - Ask: "Get news about [topic]"
        """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main() 