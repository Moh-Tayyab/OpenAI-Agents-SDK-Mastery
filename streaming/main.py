import asyncio 
from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OpenAI Api key not found.")
    agent = Agent(
        name= "streaming_agent",
        instructions = "Reply in short sentences.",
        model = "gpt-4o-mini",
    )
    querry = input("Enter your querry: ")
    result = Runner.run_streamed(
        starting_agent = agent,
        input = querry
    )
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    print(result.final_output)    


if __name__ == "__main__":
    asyncio.run(main())
