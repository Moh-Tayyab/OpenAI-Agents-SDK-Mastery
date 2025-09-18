from pydantic import BaseModel, Field
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
import rich
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

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
    

    class bank_info(BaseModel):
        account_num: str = Field(description="")
        rout_num: int
        amount: float

    # Global bank agent definition
    bank_agent = Agent(
        name="bank_info_agent",
        instructions="You are a banking agent. You will collect bank information from users. if uers add invalid info to stop it.",
        model="gpt-4o-mini",
        output_type=bank_info
    )
    
    @input_guardrail
    async def bank_info_check(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem])-> GuardrailFunctionOutput:
        
        guardrail_result = await Runner.run(
            bank_agent,
            input,
            context=ctx
        )
        return  GuardrailFunctionOutput(
            output_info = guardrail_result.final_output,
            tripwire_triggered = guardrail_result.final_output.bank_info
        ) 

    # Customer service agent with guardrail
    customer_service_agent = Agent(
        name="customer_service_agent",
        instructions="You are a customer service agent. You will assist users with their banking issues.",
        model="gpt-4o-mini",
        input_guardrails=[bank_info_check]
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
    
    
    