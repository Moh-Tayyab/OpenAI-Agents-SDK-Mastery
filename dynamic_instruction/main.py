from agents import Agent, Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio
from dotenv import load_dotenv
from agents.run import RunConfig
import os

load_dotenv()

async def main():
    MODEL_NAME = "gemini-2.0-flash"
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise ValueError("Gemini Api key not found.")
    client = AsyncOpenAI(
        api_key=API_KEY, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
    # API_KEY = os.getenv("OPENAI_API_KEY")
    # if not API_KEY:
    #     raise ValueError("OpenAI Api key not found.")
    
    config=RunConfig(
        model=model,
        model_provider=client
    )
    class PythonUser:
        reasoning: str
        yes_or_no: bool
    
    async def my_dynamic_instruction(wrapper: RunContextWrapper[PythonUser], agent: Agent) -> str:
        # Direct string input access
        user_text = str(getattr(wrapper.context, "input", [])) or []
        if "Math_Home_Work" in user_text:
            return f"You are {agent.name}, explain Python like I'm a complete beginner."
        elif "advanced" in user_text:
            return f"You are {agent.name}, explain with advanced technical details."
        else:
            return f"You are {agent.name}, explain Python programming clearly and concisely."


    user=PythonUser()
    agent=Agent(
        name="Python Helper",
        instructions=user.my_dynamic_instruction(),
        model=model,
        #model_settings=ModelSettings(temparture=0.1, max_tokens=100)
    )  
    
    querry= input("Ask me anything about python programming: ")
    result= await Runner.run(
        agent, 
        input= querry,
        config=config,
        context=user
    )
    print(result.final_output)
    
if __name__ == "__main__":
   asyncio.run(main())