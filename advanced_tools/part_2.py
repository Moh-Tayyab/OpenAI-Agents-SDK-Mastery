# tool choice and is_enabled 
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings

from dotenv import load_dotenv

from agents.run import RunConfig

import asyncio

import os

load_dotenv()

async def main():
	gemini_api= os.getenv("GEMINI_API_KEY")
	if not gemini_api:
			raise ValueError("api key is not found.")
	client=AsyncOpenAI(
			api_key=gemini_api,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	)
		
	model=OpenAIChatCompletionsModel(
			model="gemini-2.0-flash",
			openai_client=client
	)
		
	config=RunConfig(
			model=model,
			model_provider=client
	) 
	@function_tool(is_enabled=False, name_override="weather")# aider mene tool ko disable kr diye hai
	def fetch_weather() -> str:
		"""Fetch the weather for a given location."""
		return "sunny"
	
	agent = Agent(
		name ="weather assistant",
		instructions = "you are helpful assistant help about weather",
		tools = [fetch_weather],
		model_settings = ModelSettings(
		tool_choice="required" # ab hum na require kr diye hai jb bhi agent run ho ga tu tool call ho ga
  )
	)
	
	result = await Runner.run(
		starting_agent=agent,
		input="what is today weather in lahore",
		run_config=config
	)
	print(result.final_output)

if __name__ == "__main__":
	asyncio.run(main())
		