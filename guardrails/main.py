from pydantic import BaseModel
from agents import (
    Agent, Runner, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
)

class bank_info(BaseModel):
    account_num: str
    rout_num: str
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
    agent: Agent,
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

# Test function
async def test_bank_info():
    try:
        result = await Runner.run(
            customer_service_agent,
            "Help me with my bank account. My account number is 000000000 and routing number is 123456789. I want to transfer $1000."
        )
        print("Guardrail failed - this should not print")
    except InputGuardrailTripwireTriggered as e:
     print("Tripwire triggered:", e)
     print("Guardrail output:", e.guardrail_output.output_info)
