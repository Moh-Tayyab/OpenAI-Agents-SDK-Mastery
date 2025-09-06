from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper
from agents.run import RunConfig
from dotenv import load_dotenv
from dataclasses import dataclass
#import datetime 
import os
import asyncio
load_dotenv()

async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("api key not found.")
    
    client=AsyncOpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    
    config=RunConfig(
        model=model,
        model_provider=client
        )
    
    @dataclass
    class TravelUser:
        name: str
        #destination: str
        #date: str
        passport_num: int
    
    @function_tool
    def book_ticket(wrapper: RunContextWrapper[TravelUser], destination: str) -> str:
        user=wrapper.context
        """Search for flights to a destination on a specific date."""
        return f"Booking flight for {user.name} (Passport: {user.passport_num}) to {destination} with a preference for WINDOW seats."
    #{datetime.datetime.now().strftime('%H:%M:%S')}
    agent=Agent(
        name="Booking_Assistant",
        instructions=" You are a travel booking assistant. The user prefers WINDOW seats. Always consider this preference when booking.",
        model=model,
        tools=[book_ticket]
    )
    user= TravelUser(name="John Doe", passport_num=123456789)
    querry= input("Enter your query: ")
    
    result= await Runner.run(
        starting_agent=agent,
        input=querry,
        run_config=config,
        context=user
    )
    
    print(result.final_output)
    
    

if __name__ == "__main__":
    asyncio.run(main())