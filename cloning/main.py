from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


async def main():
    gemini_key= os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("api key is not found!")
        
    client=AsyncOpenAI(
         api_key=gemini_key,
          base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
     )   
    
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
    @function_tool
    def clean_data():
        return f"cleaning the data"
    
    agent=Agent(
        name="data checker",
        instructions="you are expert ai agent, your responsibilities to check data and give summary.",
        
    )
    
    result= await Runner.run(
        starting_agent=agent,
        input="summarize and cleaning data"
    )
      
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
