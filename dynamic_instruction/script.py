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

@dataclass
class UserInfo:
    name: str
    age: int
    email: str
    def dynamic_instruction(self) -> str:
        #print("context in dynamic instruction:", wrapper.context)
        return f"python helper assistant? name: {self.name} and age = {self.age}"

@function_tool
def browse(wrapper: RunContextWrapper[UserInfo]) -> str:
    """search the web for user"""
    print("context:", wrapper.context)
    return f"user info"

user = UserInfo(name="Tayyab", age=22, email="abc@gmail.com")

# def dynamic_instruction(wrapper: RunContextWrapper, agent: Agent) -> str:
#     print("context in dynamic instruction:", wrapper.context)
#     return f"python helper assistant? agent name: {agent.name} and username = {wrapper.context.name}"
    
agent=Agent(
    name="python_helper",
    instructions=user.dynamic_instruction(),
    tools=[browse]
) 

result = Runner.run_sync(
 starting_agent=agent,
 input="what is user name and age?",
 run_config=config,
 context=user
)

print(result.final_output)

