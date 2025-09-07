from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionModels
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
    
    model=OpenAIChatCompletionModels(
        model=model,
        openai_client=client
    )
    
    agent=Agent(
        name="",
        instructions="",
        
    )
    
    result= await Runner.run_sync(
        starting_agent=agent,
        input=""
    )
      
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
