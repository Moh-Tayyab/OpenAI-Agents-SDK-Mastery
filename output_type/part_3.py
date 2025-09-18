# pydantic and dataclas output

from dataclasses import dataclass
from typing import Dict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from typing import TypedDict
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
class Is_Check(BaseModel):
    is_name: bool = Field(description = "if user name is avalabile it's value will be true otherwise false")
# pydatic class not be wrapped
class Is_Check(BaseModel):
    is_name:str


# dataclass would be wrapped
@dataclass    
class Is_Check():
    is_name:str

# no wrap will treat it like normal pydantic classes
@dataclass    
class Is_Check(BaseModel):
    is_name:str

# will not be wrapped
class Is_Check(TypedDict):
    is_name:str
    

agent = Agent(  
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=Is_Check  
)

async def main():
    
    result = await Runner.run(agent, "hi, how are you, tayyab is here how you assist", run_config=config)
    print(result.final_output)

asyncio.run(main())


