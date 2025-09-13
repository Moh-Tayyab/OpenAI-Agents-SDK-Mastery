from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, StopAtTools

from dotenv import load_dotenv

from agents.run import RunConfig

import asyncio

import os

load_dotenv()

async def main():
	gemini_api=os.getenv("GEMINI_API_KEY")
	if not gemini_api:
			raise ValueError("api key is not found.")
	client=AsyncOpenAI(
			api_key=gemini_key,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	)
		
	model=OpenAIChatCompletionsModel(
			model="gemini-2.0-flash",
			model_provider=client
	)
		
	config=RunConfig(
			model=model,
			openai_client=client
	)
	@function_tool(name_override = "weather")    #name override
	async def fetch_weather(location: dict[str, float]) -> str:
		"""Fetch the weather for a given location."""
		return "sunny"
	
	agent = Agent(
		name ="",
		instructions = "",
		tools = [fetch_weather],
		tool_use_behaviour =StopAtTools(stop_at_tools_names= [fetch_weather]) # aider mene required kr diye hai ky bas is tool ky baad stop yahni yh he final output ho ge.	
	)
	
	result = await Runner.run(
		starting_agent=agent,
		input="input",
		run_config=config
		
	)
	print(result.final_output)

if __name__ == "__main__":
		asyncio.run(main())
		