import asyncio 
from agents import Agent, Runner, enable_verbose_stdout_logging, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from agents.run import RunConfig
from dotenv import load_dotenv
import os
from rich import print
load_dotenv()

# enable_verbose_stdout_logging()

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
    @function_tool
    async def get_weather(city: str) -> str:
        print("\n[BEFORE SLEEP]\n")
        await asyncio.sleep(5)
        print("\n[AFTER AWAKE NOW]\n")
        return f"The weather in {city} is sunny."
    
    @function_tool
    def enhance_text(text: str) -> str:
        return f"Enhanced text: {text}!!!"
    agent = Agent(
        name= "streaming_agent",
        instructions = "You are a expert AI Agent.",
        model = model,
        tools = [get_weather, enhance_text]
    )
    #query = input("user query: ")
    result = Runner.run_streamed(
        starting_agent = agent,
        input = "What is weather in karachi?'"
    )
    
    async for event in result.stream_events():
        #print(f"\n[Event]: {event}")
        # if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #     print(f"[Data]: {event.data.delta}")
        #     if isinstance(event.data, ResponseTextDeltaEvent):
        #         print(f"[bold green]{event.data.delta}[/bold green]", end="", flush=True)                                    
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
    # print(result.final_output)    


if __name__ == "__main__":
    asyncio.run(main())
