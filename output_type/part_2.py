# AgentOutputSchema 
# use AgentOutputSchema if you want to disable strict JSON schema

from dataclasses import dataclass
from typing import Dict
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    AgentOutputSchema,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

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


# pydantic class
class DevOutput(BaseModel):
    html: str
    css: str

    

agent = Agent(  
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=AgentOutputSchema(DevOutput, strict_json_schema=False)  
)

async def main():
    
    result = await Runner.run(agent, "what is HTML and CSS?", run_config=config)
    print(result.final_output)

asyncio.run(main())


