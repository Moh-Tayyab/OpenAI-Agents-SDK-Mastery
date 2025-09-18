# parallel_tool_calls, 
from agents import (
    Agent, Runner, 
    function_tool, 
    AsyncOpenAI, 
    OpenAIChatCompletionsModel, 
    ModelSettings, StopAtTools, 
    enable_verbose_stdout_logging,  
    set_default_openai_client,
    set_tracing_disabled,
    set_default_openai_api
    )
from dotenv import load_dotenv
from agents.run import RunConfig
from rich import print
import asyncio

import os

load_dotenv()

#enable_verbose_stdout_logging()



async def main():
    
	# gemini_api=os.getenv("GEMINI_API_KEY")
	# if not gemini_api:
	# 		raise ValueError("api key is not found.")
	# client=AsyncOpenAI(
	# 		api_key=gemini_api,
	# 		base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	# )
		
	# model=OpenAIChatCompletionsModel(
	# 		model="gemini-2.0-flash",
	# 		openai_client=client
	# )
		
	# config=RunConfig(
	# 		model=model,
	# 		model_provider=client
	# )
	
	#set_default_openai_client(client)
	set_tracing_disabled(disabled=True)
	set_default_openai_api("chat_completions")
 
 
	@function_tool
	def fetch_weather() -> str:
			"""Fetch the weather for a given location."""
			return "sunny"
	@function_tool
	def calculator(operations: str) -> str:
		"""
		Simple math calculator tool.
		"""
		result = eval(operations)
		return f"result:  {result}"
	
	agent = Agent(
		name ="Math Agent",
		instructions = """
						You are a helpful assistant.

						- For math questions, use the calculator tool and explain step by step.
						- For weather questions, use the fetch_weather tool.
						- For all other questions, answer directly without tools.
  						""",
		tools = [calculator, fetch_weather],
		model_settings=ModelSettings(
			tool_choice="auto",
			parallel_tool_calls=True, #Yeh feature sirf kuch OpenAI models. Google Gemini API is ko sport nhi karti.
			#include_usage=True,
			temperature=0.2,   # low randomness
            top_p=0.9,         # nucleus sampling
            top_k=50          # restrict to top 50 tokens
		),
		#tool_use_behavior =StopAtTools(stop_at_tools_names= [calculator])	
	)
 
 # Agar tum chahte ho ke empty input handle ho jaye, to simple check lagana hoga:
	query = input("user query: ").strip()
	if not query:
		query="⚠️ Please enter a valid query, empty input is not allowed."

	result = await Runner.run(
		starting_agent=agent,
		input=query,
		#run_config=config
		
	)
	print(result.final_output)

if __name__ == "__main__":
		asyncio.run(main())
		