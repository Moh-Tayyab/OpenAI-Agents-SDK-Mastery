# Tool: The hands. A tool is just a Python function.

# Pydantic for Tools:

# Understand why Pydantic is used: for automatic schema generation, input validation, and clear definitions.

# Practice creating Pydantic models for tool inputs. Know how to use Field for descriptions and default values.

from agents import Runner, Agent, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings

from pydantic import BaseModel, Field
from agents.run import RunConfig
import asyncio, os
from dotenv import load_dotenv
from typing import Optional, Dict, Union

load_dotenv()

async def main():
    API_KEy = os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
	
    AsyncOpenAI(
		api_key=API_KEy,
		base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
	)
	
    model = OpenAIChatCompletionsModel(
		model="gemini-1.5-flash",
		openai_client=AsyncOpenAI(
			api_key=API_KEy,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
		)
	)
	
    config = RunConfig(
		model=model,
	)
    class ContactInfo(BaseModel):
      """Contact information sub-model."""
      email: str = Field(..., description="Email address")
      phone: Optional[str] = Field(default=None, description="Phone number")
      
    class UserRegistrationInput(BaseModel):
        """Model for user registration tool."""
        username: str = Field(..., description="Unique username", min_length=3, max_length=50)
        password: str = Field(..., description="User password", min_length=8)
        # full_name: str = Field(..., description="User's full name", min_length=1, max_length=100)
        contact: ContactInfo = Field(..., description="Contact information")
        # age: Optional[int] = Field(default=None, description="User's age", ge=13, le=120)
        # preferences: Dict[str, Union[str, bool, int]] = Field(
        #     default_factory=dict, 
        #     description="User preferences as key-value pairs"
        # )
    
    @function_tool
    async def register_user(input: UserRegistrationInput):
        # Registration logic here
        return f"User {input.username}, password {input.password}, contact {input.contact.phone} registered successfully with email {input.contact.email}."


    agent = Agent(
		name="User Registration Agent",
		instructions="You are an agent that helps with user registrations. Use the register_user tool to register new users." ,
		tools=[register_user],
	)
    
    query = input("user querry: ")
    
    result = await Runner.run(
		starting_agent=agent,
        input=query,
        run_config=config
	)
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    