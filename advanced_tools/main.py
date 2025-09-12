from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("api key is not found")
    
    client = AsyncOpenAI(
		api_key = gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	)
    
    model = OpenAIChatCompletionsModel(
		model = "gemini-2.0-flash",
		openai_client = client	
    )
    
    config = RunConfig(
		model = model,
		model_provider = client
	)
    
    @function_tool 
    def webSearch():
        return 
    
    
    agent = Agent(
		name = "",
		instructions = "",
		tools = [webSearch]
  	)
    
    result = await Runner.run(
		starting_agent = agent,
		input = "",
		run_config = config
	)
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())   