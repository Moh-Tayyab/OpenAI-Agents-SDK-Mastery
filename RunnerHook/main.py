#from multiprocessing import context
from agents import Agent, RunHooks, Runner
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

class MyRunnerHook(RunHooks):
    async def on_run_start(self, config) -> str:
        print(f"Run started with config:")

    async def on_run_end(self, context, result) -> str:
        print(f"Run ended with final output:")

    async def on_agent_start(self, context, input) -> str:
        print(f"Agent started with input: ")
        print(f"Context info: ")

    async def on_agent_end(self, context, result) -> str:
        print(f"Agent ended with output: ")
        print(f"Context info: ")

    async def on_tool_start(self, tool, input) -> str:
        print(f"Tool started with input: ")

    async def on_tool_end(self, tool, output) -> str:
        print(f"Tool ended with result: ")

    async def on_handoff(self, context=None, from_agent=None, to_agent=None, input=None) -> str:
        print(f"Handoff from to with input: ")
        print(f"Context info: ")

async def main():
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OpenAI API key not found.")
    
    booking_agent = Agent(
        name="BookingAgent",
        instructions="An agent that handles booking tasks."
    )
    refund_agent = Agent(
        name="RefundAgent",
        instructions="An agent that processes refund requests."
    )
    
    triage_agent = Agent(
        name="TriageAgent",
        instructions="If the request is about booking → handoff to BookingAgent; if about refund → handoff to RefundAgent.",
        handoffs=[booking_agent, refund_agent]
    )
    
    result = await Runner.run(
        starting_agent=triage_agent,
        input="I want to book a flight and also need a refund for my last booking.",
        hooks=MyRunnerHook()
    )
    
    print(f"\n✅ Final Output: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
