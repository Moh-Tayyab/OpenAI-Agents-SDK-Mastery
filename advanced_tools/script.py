# advanced_tools/script.py
import asyncio
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr

from agents import (
    Runner,
    Agent,
    function_tool,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
)
from agents.run import RunConfig

load_dotenv()

# --- 1) create a single async client and model ---
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY or OPENAI_API_KEY in your environment")

openai_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=openai_client,
)

run_config = RunConfig(model=model)

# --- 2) Pydantic models (defined at module level) ---
class ContactInfo(BaseModel):
    """Contact information sub-model."""
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")

class UserRegistrationInput(BaseModel):
    username: str = Field(..., description="Unique username", min_length=3, max_length=50)
    password: str = Field(..., description="User password", min_length=8)
    contact: ContactInfo = Field(..., description="Contact information")
    user_id: Optional[str] = Field(default=None, description="User ID if updating an existing user")

# --- 3) custom failure handler ---
def my_custom_error_function(context: RunContextWrapper, error: Exception) -> str:
    # Log the error server-side (do not reveal internals to users)
    print("Tool call failed:", repr(error))
    # You can inspect `context` if you want: print(context.input) etc.
    return "An internal server error occurred. Please try again later."

# --- 4) tools exposed to the agent ---
@function_tool
async def register_user(input: UserRegistrationInput) -> str:
    # NOTE: DO NOT store or log the plaintext password in production.
    # Instead: hash the password and store user record in DB asynchronously.
    # Example (pseudo):
    # hashed = await async_hash_password(input.password)
    # user_id = await db.create_user(username=input.username, password=hashed, contact=input.contact.dict())
    return (
        f"User '{input.username}' registered successfully "
        f"(email={input.contact.email}, phone={input.contact.phone})"
    )
from models import SessionLocal, User

@function_tool(name_override="user")
async def register_user(input: UserRegistrationInput):
    session = SessionLocal()
    try:
        new_user = User(
            username=input.username,
            password=input.password,   # ⚠️ In real apps, hash this!
            email=input.contact.email,
            phone=input.contact.phone
        )
        session.add(new_user)
        session.commit()
        return f"User {input.username} registered successfully with email {input.contact.email}."
    except Exception as e:
        session.rollback()
        return f"Error registering user: {e}"
    finally:
        session.close()
        
@function_tool(failure_error_function=my_custom_error_function)
def get_user_profile(user_id: str) -> str:
    # Example mock: simulate DB / external API
    if user_id == "user_123":
        return "User profile for user_123 successfully retrieved."
    raise ValueError(f"Could not retrieve profile for user_id: {user_id}. API returned an error.")

# --- 5) build and run the agent ---
async def main():
    agent = Agent(
        name="User Registration Agent",
        instructions=(
            "You are an agent that helps with user registration and profile retrieval. "
            "Use the provided tools (register_user, get_user_profile) to fulfil user requests."
        ),
        
        model=model,
        tools=[register_user, get_user_profile],
    )

    query = input("user query: ")  # e.g. "Register a user with username mike, password Abc12345, email mike@example.com"
    result = await Runner.run(starting_agent=agent, input=query, run_config=run_config)

    # Runner result shape can vary by SDK version; print available fields for debugging:
    #final = getattr(result, "final_output", None) or getattr(result, "output", None) or result
    print("=== Agent result ===")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
