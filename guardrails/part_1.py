# simple input guardrails without agents
# input guardrails run only first agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

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
class Is_Teacher(BaseModel):
    is_teacher: bool = Field(description= "if is teacher guardrials will work fine")
    
teacher_agent = Agent(  
    name="teacher_agent",
    instructions="You are a teacher agent. You help students with their questions.",
    output_type=Is_Teacher
)
    
    
# function is required in InputGuardrails
@input_guardrail
async def check_teacher(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    teacher_result = await Runner.run(
        teacher_agent,
        input,
        context = ctx
    )
    return GuardrailFunctionOutput(
        output_info= teacher_result.final_output,
        tripwire_triggered = teacher_agent.final_out.is_teacher
    )
# function is required in InputGuardrail 
# @input_guardrail
# async def hacking_guardrail( 
#     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     return GuardrailFunctionOutput(
#         output_info=None, 
#         tripwire_triggered=False,
#     )
agent = Agent(  
    name="Guardrail Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[check_teacher],
    model=model
)

# agent = Agent(  
#     name="Customer support agent",
#     instructions="You are a customer support agent. You help customers with their questions.",
#     input_guardrails=[hacking_guardrail],
#     model=model
# )

async def main():
    query=input
    try:
        result = await Runner.run(agent, input=query, run_config=config)
        print(result.final_output)
        print(result.last_agent)
        print("Guardrail didn't trip")

    except InputGuardrailTripwireTriggered as e:
        print("guardrail tripped")
        print(e.guardrail_result.output)

asyncio.run(main())