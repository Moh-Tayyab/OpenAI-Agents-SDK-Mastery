from agents import Runner, Agent
import asyncio
import os
from dotenv import load_dotenv
import chainlit as cl
load_dotenv()

@cl.on_message
async def main(message: cl.message):
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OpenAI Api key not found.")
    
    booking_agent = Agent(
        name = "Booking Agent",
        instructions = "Handle booking inquiries"
    )
    refund_agent = Agent(
        name = "Refund Agent",
        instructions = "process refund inquiries"
    )
    
    tri_agent = Agent(
        name = "Triage Agent",
        instructions =  "You are a helpdesk agent."
        "If the user asks about booking, hand off to the Booking agent."
        "If about refunds, hand off to the Refund agent.",
        model = "gpt-4o-mini",
        handoffs = [booking_agent, refund_agent]
    )
    
    result = await Runner.run(
        starting_agent = tri_agent,
        input = message.content
    )
    await cl.Message(content=result.final_output).send()
    #print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
