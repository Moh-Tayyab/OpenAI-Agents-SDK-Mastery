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

    config=RunConfig(
        model=model,
        model_provider=client
    )
    class PythonUser:
        reasoning: str
        yes_or_no: bool
        def __init__(self, query: str = "") -> str:
          self.query = query
    
     #✅ dynamic instruction must accept (context, agent)
    async def my_dynamic_instruction(wrapper: RunContextWrapper[PythonUser], agent: Agent) -> str:
        # ✅ Get user input directly
        user_text = getattr(wrapper.context, "query", "")
        if "beginner" in user_text:
            return f"You are {agent.name}, explain Python like I'm a complete beginner."
        elif "intermediate" in user_text:
            return f"You are {agent.name}, explain with moderate technical details."
        elif "advanced" in user_text:
            return f"You are {agent.name}, explain with advanced technical details."
        else:
            return f"You are {agent.name}, explain Python programming clearly and concisely."


    agent=Agent(
        name="Python Helper",
        instructions=my_dynamic_instruction, #✅ passing function reference not calling it
        model=model,
    )  
    
    query= input("Ask me anything about python programming: ")
    user = PythonUser(query=query)
    result=await Runner.run(
        agent, 
        input= query,
        run_config=config,
        context=user
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
   asyncio.run(main())