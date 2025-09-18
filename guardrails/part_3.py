#output guardrails
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
import rich
from typing import Any

async def main():
	API_KEY=os.environ.get("GEMINI_API_KEY")
	OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

	model=OpenAIChatCompletionsModel(
		model="gemini-1.5-flash",
		openai_client=AsyncOpenAI(
			api_key=API_KEY,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
		)
	)

	config=RunConfig(
		model=model
	)

	class President_class(BaseModel):
		is_persident: bool


	guardrail_agent = Agent(
		name="Guardrail Agent",
		instructions="You are check user is asking about president ot not",
		output_type=President_class
	)

	@output_guardrail
	async def check_president(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
		guardrail_result = await Runner.run(
			guardrail_agent,
			output,
			context=ctx
		)
		return GuardrailFunctionOutput(
			output_info= guardrail_result.final_output,
			tripwire_triggered=guardrail_result.final_output.is_president
		)

	agent = Agent(  
		name="Guardrail Agent",
		instructions="You are a expert AI Agent.",
		output_guardrails=[check_president],
		model=model
	)
	

	try: 
		# 10 result   
			query=input("user query: ")
			result = await Runner.run(
				starting_agent = agent,
				input= query,
				run_config = config
				)
			print("Guardrail failed - this should not print")
	except OutputGuardrailTripwireTriggered as e:
			print("❌ 🚨 Tripwire triggered!", e)
			#print("Final Output:", e.guardrail_result.final_output.output_info)  # ✅
			#print("Tripwire Value:", e.guardrail_result.tripwire_triggered)      # ✅

        
	print(result.final_output) # 11 final_output
 
if __name__ == "__main__":
    asyncio.run(main())