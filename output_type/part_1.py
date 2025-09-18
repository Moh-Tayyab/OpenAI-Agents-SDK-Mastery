# any output type
from pydantic import BaseModel
from typing import TypedDict
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)
from agents.run import RunConfig
import rich

load_dotenv()


async def main():
    API_KEY=os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

    model=OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=AsyncOpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        )

    config=RunConfig(
        model=model
        )
    class WeatherReport(BaseModel):
            location: str
            temperature: float
            condition: str
            
    class WeatherReport(TypedDict):
            location: str
            temperature: float
            condition: str        
                 
            
    agent = Agent(  
            name=" WeatherAgent",
            instructions="You are a expert AI Agent.",
            output_type=WeatherReport,  # 👈 enforcing structured output 
            output_type=list[WeatherReport]
        )
        

    query=input("user query: ")
    result = await Runner.run(
            starting_agent = agent,
            input= query,
            run_config = config
            )
    print("Structured Output:", result.final_output)
 
if __name__ == "__main__":
    asyncio.run(main())