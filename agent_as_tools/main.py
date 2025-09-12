#agent_as_tool
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)


gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
	raise ValueError("api key is not found")

client = AsyncOpenAI(
	api_key=gemini_key,
	base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
	model="gemini-2.0-flash",
	openai_client=client
)

config = RunConfig(
	model=model,
	model_provider=client
)

# Translator Agent
translator_agent = Agent(
	name="translator_agent",
	instructions="You are a helpful translator. Translate given text into the target language."
)

# Summarizer Agent
summarizer_agent = Agent(
	name="summarizer_agent",
	instructions="You are a summarization agent. Summarize long text clearly and concisely."
)

# Knowledge Agent
knowledge_agent = Agent(
	name="knowledge_agent",
	instructions="You are a knowledge assistant. Answer factual questions accurately."
)

translate_to_spanish = translator_agent.as_tool(
	tool_name="translator",
	tool_description="Translate text into a target language."
)
summarize_text = summarizer_agent.as_tool(
	tool_name="summarizer",
	tool_description="Summarize long text."
)
knowledge = knowledge_agent.as_tool(
	tool_name="knowledge",
	tool_description="Answer factual questions."
)

main_agent = Agent(
	name="Main Agent",
	instructions=(
		"You are the main coordinator agent. Decide which tool-agent to use "
		"based on the user's request. Use translator for 'translate into', "
		"summarizer for long text, and knowledge agent for factual questions."
	),
	tools=[translate_to_spanish, summarize_text, knowledge],
	model=model
)
async def main():
	print(">>> Translate Example")
	result = await Runner.run(
		starting_agent=main_agent,
		input="Translate 'hello world' into Spanish",
		run_config=config
	)
	print(result.final_output)
	print("\n")

	print(">>> Summarize Example")
	result = await Runner.run(
		starting_agent=main_agent,
		input="This is a very long text which definitely needs summarization because it's lengthy and repeating again and again to cross threshold...",
		run_config=config
	)
	print(result.final_output)
	print("\n")

	print(">>> Knowledge Example")
	result = await Runner.run(
		starting_agent=main_agent,
		input="Who is the Prime Minister of Pakistan?",
		run_config=config
	)
	print(result.final_output)
	print("\n")

	print(">>> Invalid Example")
	result = await Runner.run(
		starting_agent=main_agent,
		input="Summarize",
		run_config=config
	)
	print(result.final_output)
	print("\n")

	# result = await Runner.run(
	#     starting_agent = main_agent,
	#     input = "",
	#     run_config = config
	# )

	# print(result.final_output)


if __name__ == "__main__":
	asyncio.run(main())