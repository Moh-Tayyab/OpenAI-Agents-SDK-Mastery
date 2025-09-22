from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, set_tracing_disable

from openai.types.response import ResponseTextDeltaEvent

from agents.run import RunConfig

from dotenv import load_dotenv

load_dotenv()

enable_verbrose_stdout_logging()


async def main():
    
    agent = Agent(
		name = None,
		instructions = "you are a helpful assistant"
	)

if __name__ == "__main__":
    asyncio.run(main())    