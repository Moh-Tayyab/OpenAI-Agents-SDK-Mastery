from agents import Agent, Runner
from agents.tool import function_tool
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import os
import datetime
import random
from dotenv import load_dotenv
load_dotenv()

async def main():
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OpenAI Api key not found.")
    
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
    
    agent = Agent(
        name = "HelperBot",
        instructions="You can tell a joke or tell the time depending on user input.",
        model="gpt-4o-mini",
        tools=[time_tool_obj, joke_tool_obj],
        tool_use_behavior = "stop"
    )
    
    querry=input("Please choice one option u know current time or tech joke: ")
    
    result = Runner.run_streamed(
        starting_agent=agent,
        input=querry,
    )
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



