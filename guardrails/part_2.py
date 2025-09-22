from pydantic import BaseModel, Field
from agents import (
    Agent, Runner, 
    GuardrailFunctionOutput, 
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings)
import rich
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio, os
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
    class Bank_Info(BaseModel): # 7 bank_info
        account_num: str = Field(description="")
        rout_num: int
        amount: float

    # Global bank agent definition
    bank_agent = Agent( # 6 bank_agent
        name="bank_info_agent",
        instructions="You are a banking agent. You will collect bank information from users. if uers add invalid info to stop it.",
        model="gpt-4o-mini",
        output_type=Bank_Info
    )
    
    @input_guardrail                                                # 3 input
    async def bank_info_check(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem])-> GuardrailFunctionOutput:
    # 8 guardrail_result         # 4 runner
        guardrail_result = await Runner.run(
            bank_agent, # 5 bank_agent
            input,
            context=ctx
        )
        return  GuardrailFunctionOutput(
            output_info = guardrail_result.final_output, # 9 output_info
            tripwire_triggered =  len(guardrail_result.final_output.account_num) >= 10 
            # tripwire_triggered = False # True/False # 10 tripwire_triggered  
        ) 

    # Customer service agent with guardrail
    customer_service_agent = Agent( # 2 agent
        name="customer_service_agent",
        instructions="You are a customer service agent. You will assist users with their banking issues.",
        model="gpt-4o-mini",
        input_guardrails=[bank_info_check],
        model_settings=ModelSettings(
            max_tokens= 100
        )
    )  

    try: 
    # 10 result   
        result = await Runner.run(
            starting_agent = customer_service_agent,
            input= "Help me with my bank account. My account number is 000000000 and routing number is 123456789. I want to transfer $1000.", # 1 user input
            run_config = config
            )
        print("Guardrail failed - this should not print")
    except InputGuardrailTripwireTriggered as e:
        print("❌ 🚨 Tripwire triggered!", e)
        #print("Final Output:", e.guardrail_result.final_output.output_info)  # ✅
        #print("Tripwire Value:", e.guardrail_result.tripwire_triggered)      # ✅
   
    print(result.final_output) # 11 final_output
    
if __name__ == "__main__":
    asyncio.run(main())    
    
    
    