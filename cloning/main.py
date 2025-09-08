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
    
    @function_tool
    def summerize_data():
        return f"summerizing the data"
    
    agent1=Agent(
        name="data checker",
        instructions="you are expert ai agent, your responsibilities to check data and give summary.",
        tools=[clean_data]
    )
    
    agent2=agent1.clone(
        tools=[summerize_data]
    )
    
    result= await Runner.run(
        starting_agent=agent1,
        input="summarize and cleaning data"
    )
      
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
