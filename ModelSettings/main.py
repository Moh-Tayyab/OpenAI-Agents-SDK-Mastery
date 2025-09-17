# stop at first tool concept.
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, enable_verbose_stdout_logging
from dotenv import load_dotenv
from agents.run import RunConfig
from rich import print
import asyncio

import os

load_dotenv()

#enable_verbose_stdout_logging()


async def main():
	gemini_api=os.getenv("GEMINI_API_KEY")
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
	@function_tool
	def calculator(operations: str) -> str:
		"""
		Simple math calculator tool.
		"""
		result = eval(operations)
		return f"result:  {result}"
	
	agent = Agent(
		name ="Math Agent",
		instructions = "You are helpful math tutor, who willl solve math problem with details like how this answer solve",
		tools = [calculator],
		model_settings=ModelSettings(
			tool_choice="required",
			#include_usage=True,
			temperature=0.2,   # low randomness
            top_p=0.9,         # nucleus sampling
            top_k=50           # restrict to top 50 tokens
		)
		#tool_use_behaviour =StopAtTools(stop_at_tools_names= [fetch_weather])	
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
		