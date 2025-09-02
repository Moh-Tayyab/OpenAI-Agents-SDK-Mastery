#context_dynamic_instruction

from agents import Runner, RunContextWrapper, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
	api_key=gemini_key,
	base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(
	model=llm_model,
    model_provider=client,
    #tracing_disable= True
)

@function_tool
def user_info():
    return f"user info"
agent=Agent(
    name="helping_assistant",
    instructions="you are a assistant to help user."
)
result = Runner.run_sync(
 starting_agent=agent,
 input="hi",
 run_config=config,
 context={"name": "Tayyab"}
)

print(result.final_output)

