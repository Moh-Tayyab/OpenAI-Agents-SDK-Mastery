#agent_as_tool
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

async def main():
    
		gemini_key = os.getenv("GEMINI_API_KEY")
		if not gemini_key:
			raise ValueError("api key is not found")
		
		client = AsyncOpenAI(
			api_key = gemini_key,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
		)
		
		model = OpenAIChatCompletionsModel(
			model = "gemini-2.0-flash",
			openai_client = client	
		)
		
		config = RunConfig(
			model = model,
			model_provider = client
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

		main_agent = Agent(
			name = "Main Agent",
			instructions="You are the main coordinator agent. Decide which tool-agent to use "
                 "based on the user's request. Use translator for 'translate into', "
                 "summarizer for long text, and knowledge agent for factual questions.",
			tools = [
				translator_agent.as_tool("translator", description="Translate text into a target language."),
				summarizer_agent.as_tool("summarizer", description="Summarize long text."),
				knowledge_agent.as_tool("knowledge", description="Answer factual questions.")
			]
		)

		print(">>> Translate Example")
		async for event in main_agent.run("Translate 'hello world' into Spanish"):
			if event.type == "response.output_text.delta":
				print(event.delta, end="")
		print("\n")

		print(">>> Summarize Example")
		async for event in main_agent.run("This is a very long text which definitely needs summarization "
										"because it's lengthy and repeating again and again to cross threshold..."):
			if event.type == "response.output_text.delta":
				print(event.delta, end="")
		print("\n")

		print(">>> Knowledge Example")
		async for event in main_agent.run("Who is the Prime Minister of Pakistan?"):
			if event.type == "response.output_text.delta":
				print(event.delta, end="")
		print("\n")

		print(">>> Invalid Example")
		async for event in main_agent.run("Summarize"):
			if event.type == "response.output_text.delta":
				print(event.delta, end="")
		print("\n")
			
		# result = await Runner.run(
		# 	starting_agent = main_agent,
		# 	input = "",
		# 	run_config = config
		# )
		
		#print(result.final_output)
  
		
if __name__ == "__main__":
    asyncio.run(main())   