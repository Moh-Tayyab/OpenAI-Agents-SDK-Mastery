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
		
	@function_tool(
		name_override="ChargeCard",
		description_override="Charge the user's card and return transaction id on success.",
		is_enabled=False,  # disabled in dev env
		failure_error_function=lambda exc: {"error": "payment_failed", "message": str(exc)}
	)
	def charge_credit_card(card_number: str, amount: float):
		# actual payment logic (disabled in dev)
		return f"{card_number}, {amount}"
	agent = Agent(
		name ="weather assistant",
		instructions = "You are a professional ecommerce store assistant.",
		tools = [charge_credit_card],
		#tool_use_behavior=StopAtTools(stop_at_tool_names=["fetch_weather"])# weather ka tool call karna ky baad ruk jy ga. or final output dy ga
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
		