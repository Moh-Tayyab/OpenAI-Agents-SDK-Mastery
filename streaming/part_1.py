
# streaming/part_1.py
# in this example i will show how you handle streaming error with tools and in streaming response

from agents import Agent, Runner, enable_verbose_stdout_logging, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel

from dotenv import load_dotenv

from agents.run import RunConfig

import asyncio, os

from openai.types.responses import ResponseTextDeltaEvent


load_dotenv()
#enable_verbose_stdout_logging()

async def main():
	API_KEy = os.environ.get("GEMINI_API_KEY")
	OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
	
	AsyncOpenAI(
		api_key=API_KEy,
		base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
	
	)
	
	model = OpenAIChatCompletionsModel(
		model="gemini-1.5-flash",
		openai_client=AsyncOpenAI(
			api_key=API_KEy,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
		)
	)
	
	config = RunConfig(
		model=model,
	)
	
	@function_tool(name_override = "weather")
	def weather_tool(city: str) -> str:
		# try:
			# suppose API call fail ho gayi
			raise TimeoutError("API not responding")
		# except Exception as e:
			# return f"Fallback: Sorry, weather data not available right now. ({e})"

	
	agent = Agent(
		name="tool_streeaming_agent",
		instructions="you are a helful assistant",
		model="gpt-4o-mini",
		tools=[weather_tool]
	)
	
	query = input("user querry: ")
	result = Runner.run_streamed(
		starting_agent=agent,
		input=query,
		run_config=config
	)
	
	async for event in result.stream_events():
		if event.type == "raw-response_event" and isinstance(event.data, ResponseTextDeltaEvent):
			print(f"[DATA]: {event.data.delta}")
			
		elif event.type == "response.tool_error":
			print("\n[⚠️ Tool Failed, using fallback...]")
			yield_text = "Fallback: Sorry, weather data is not available right now."
			print(f"[DATA]: {yield_text}")   
   
	print("\n [FINAL OUTPUT]:", result.final_output)
 
if __name__ == "__main__":
     asyncio.run(main())