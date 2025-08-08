from agents import Agent, Runner
from agents.tool import function_tool
import asyncio
import os
import datetime
import random
from dotenv import load_dotenv
load_dotenv()

async def test_tools():
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        print("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return
    
    def joke_tool() -> str:
        jokes = [
            "Why did the AI cross the road? To optimize traffic!",
            "I told the computer I needed a break—it said 'Syntax error!'"
        ]
        return random.choice(jokes)
    
    def time_tool() -> str:
         return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    
    joke_tool_obj = function_tool(
        joke_tool,
        name_override="tell-joke",
        description_override="Tells a random tech joke."
    )
    
    time_tool_obj = function_tool(
        time_tool,
        name_override="get_time",
        description_override="Returns the current system time"
    )
    
    print("✅ Tools created successfully!")
    print(f"Joke tool: {joke_tool_obj}")
    print(f"Time tool: {time_tool_obj}")
    
    # Test the tools directly
    print(f"\n🔧 Testing joke tool: {joke_tool()}")
    print(f"🔧 Testing time tool: {time_tool()}")
    
    print("\n✅ All tests passed! The original _griffe error has been resolved.")

if __name__ == "__main__":
    asyncio.run(test_tools()) 