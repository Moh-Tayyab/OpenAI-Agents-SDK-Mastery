from pydantic import BaseModel
from agents import (
    Agent, Runner, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel
    
)
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("api key not found.")
    
    client=AsyncOpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    
    config=RunConfig(
        model=model,
        model_provider=client
        )
    

    class bank_info(BaseModel):
        account_num: str
        rout_num: int
        amount: float

    # Global bank agent definition
    bank_agent = Agent(
        name="bank_info_agent",
        instructions="You are a banking agent. You will collect bank information from users.",
        model="gpt-4o-mini",
        output_type=bank_info
    )

    @input_guardrail
    async def bank_guardrail(
        ctx: RunContextWrapper[None],
        bank_agent: Agent,
        input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
        
        result = await Runner.run(
            bank_agent,
            input,
            context=ctx.context
        )
        
        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.account_num
        )

    # Customer service agent with guardrail
    customer_service_agent = Agent(
        name="customer_service_agent",
        instructions="You are a customer service agent. You will assist users with their banking issues.",
        model="gpt-4o-mini",
        input_guardrails=[bank_guardrail]
    )  


    try:
            result = await Runner.run(
                starting_agent = customer_service_agent,
            input= "Help me with my bank account. My account number is 000000000 and routing number is 123456789. I want to transfer $1000.",
            run_config = config
            )
            print("Guardrail failed - this should not print")
    except InputGuardrailTripwireTriggered as e:
            print("Tripwire triggered:", e)
            print("Guardrail output:", e.guardrail_output.output_info)
        
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    
    
    
    