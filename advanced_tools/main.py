from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel

from dotenv import load_dotenv

from agents.run import RunConfig

import asyncio

load_dotenv()

async def main():
   @function_tool
   async def fetch_weather(location: dict[str, float]) -> str:
       """Fetch the weather for a given location."""
       return "sunny"

if __name__ == "__main__":
    asyncio.run(main())
    