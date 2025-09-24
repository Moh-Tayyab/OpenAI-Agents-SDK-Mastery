# streaming/part_2.py
# in this example i will show how handle error during strweaming response with tools fetching data in db and returning fallback response
# suppose you have a tool that fetch data from db and return it to user if db is not reachable or api call fail then you return fallback response
# also i will show how to use input guardrails in streaming response
# data fetching tool will fail and return fallback response
# data fetching from momngo db

from pydantic import BaseModel, Field
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
	MONGODB_DB = os.get("MONGO_DB_URI")
	
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
				
	agent = Agent(
		name="tool_streeaming_agent",
		instructions="you are a helful assistant",
		model="gpt-4o-mini",
		tools=[]
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