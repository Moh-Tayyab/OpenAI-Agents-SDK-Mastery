import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OpenAI Api key not found.")
    agent = Agent(
        name ="Math Teacher",
        instructions = "You are a math teacher. You are given a math problem and you need to solve it.",
        model = "gpt-4o-mini",
    )
    
    result = await Runner.run(
        starting_agent = agent,
        input = "What is the square root of 16?",
    )
    print(result.final_output)    

if __name__ == "__main__":
    asyncio.run(main())
