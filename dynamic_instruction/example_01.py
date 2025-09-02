from agents import Agent, Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio
from dotenv import load_dotenv
import os
import datetime

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
    async def async_instructions(context: RunContextWrapper, agent: Agent) -> str:
    # Simulate fetching data from database
     await asyncio.sleep(0.1)
     current_time = datetime.datetime.now()
     
     return f"""You are {agent.name}, an AI assistant with real-time capabilities.
		Current time: {current_time.strftime('%H:%M')}
          Provide helpful and timely responses."""

    agent = Agent(
        name="Message Counter",
        instructions=async_instructions,
        model=model
    )

    querry= input("Ask me anything: ")
    result= await Runner.run(
		agent,
		input= querry
	)
    print(result.final_output)

if __name__ == "__main__":
   asyncio.run(main())