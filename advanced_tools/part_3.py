# tool name_override. description_override, s_enabled and tool_use_behavior concept
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, StopAtTools

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
	@function_tool(is_enabled=True, description_override=" Fetch current weather data for a given city or location.") # on/off flag, agar False to agent cannot call that tool (useful for staged rollouts).
	def fetch_weather() -> str:
		"""Fetch the weather for a given location."""
		return "sunny"
	@function_tool(name_override="news")
	def get_news() -> str:
		"""Fetch the latest news headlines for a specific topic and location.
  """
		return "A list of news headlines."
	agent = Agent(
		name ="weather assistant",
		instructions = "You are a professional weather and news assistant.",
		tools = [fetch_weather, get_news],
		tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_weather"])# weather ka tool call karna ky baad ruk jy ga. or final output dy ga
	)
	query=input("user query: ")
	result = await Runner.run(
		starting_agent=agent,
		input=query,
		run_config=config
	)
	print(result.final_output)

if __name__ == "__main__":
	asyncio.run(main())
		