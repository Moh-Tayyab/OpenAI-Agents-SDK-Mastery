# # tool name_override, description_override, is_enabled and failure_error_function concept.
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
		is_enabled=False,  # tool skip ho jayega → agent apna reply karega
		failure_error_function=lambda ctx, exc: {
        "error": "payment_failed",
        "message": str(exc)
        } # Agar function error throw kare, ye custom JSON error return karega.clean error message return kar diya
	)
	def charge_credit_card(card_number: str, amount: float):
    # Basic card number validation
			if not card_number.isdigit() or len(card_number) < 12 or len(card_number) > 19:
				raise ValueError("Invalid card number. Please provide a valid credit card number.")
			
			if amount <= 0:
				raise ValueError("Invalid amount. Payment amount must be greater than 0.")
			
			# Simulated transaction ID
			transaction_id = f"txn_{card_number[-4:]}_{int(amount*1000)}"
			return {"transaction_id": transaction_id, "amount_charged": amount}

	agent = Agent(
		name ="payment assistant",
		instructions="If the user requests to charge a credit card or make a payment, call the ChargeCard tool with the provided card number and amount.",
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
		