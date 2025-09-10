from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, handoff
import asyncio
import os
from dotenv import load_dotenv
#import chainlit as cl
load_dotenv()

#@cl.on_message
async def main():
    # API_KEY = os.getenv("OPENAI_API_KEY")
    # if not API_KEY:
    #     raise ValueError("OpenAI Api key not found.")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("api key not found.")
    
    client=AsyncOpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
    booking_agent = Agent(
        name = "Booking Agent",
        instructions = "Handle booking inquiries",
        model=model
    )
    refund_agent = Agent(
        name = "Refund Agent",
        instructions = "process refund inquiries",
        model=model
    )
    
    tri_agent = Agent(
        name = "Triage Agent",
        instructions =  "You are a helpdesk agent."
        "If the user asks about booking, hand off to the Booking agent."
        "If about refunds, hand off to the Refund agent.",
        model = model,
        handoffs=[booking_agent, handoff(refund_agent)]
    )
    query = input("user query: ")
    result = await Runner.run(
        starting_agent = tri_agent,
        #input = message.content
        input = query
    )
    #await cl.Message(content=result.final_output).send()
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
