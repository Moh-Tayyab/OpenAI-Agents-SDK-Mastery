#Customizing via handoff() function
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper
from dotenv import load_dotenv
from agents.run import RunConfig
#from agents.extensions.models.litellm_model import LitellmModel
import os 
import asyncio
#from agents import enable_verbose_stdout_logging

load_dotenv()

#enable_verbose_stdout_logging()
#set_tracing_disable(dissble=True)


async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    Model = "gemini/gemini-2.0-flash"
    if not gemini_key:
        raise ValueError("api key not found.")
    
    client=AsyncOpenAI(
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
   
    config = RunConfig(
        model=model,
        model_provider=client
    )
    
    # @function_tool
    # def route_query(query):
    #     if "linkedin" in query.lower():
    #     #yh aider custom handoff ka concept use ho rha hai
    #       return handoff(name = "LinkedIn Assistant", instructions = "You are a helpfull assitant that help to post content on linkedin.")
    #     elif "whatsapp" in query.lower():
    #         return handoff(name = "Whatsapp Assistant", instructions = "You are a helpfull assistant to handle my personal whatsapp",)
    #     else:
    #         return "I can’t find a suitable assistant."
        
        #basic hands off
    # linkedin_agent = Agent(
    #     name = "LinkedIn Assistant",
    #     instructions = "You only solve query about linkedin."
    # )
    
    # whatsapp_agent = Agent(
    #     name = "Whatsapp Assistant",
    #     instructions = "You only solve query about whatsapp"
    # )
    
    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        agent_name = agent.name
        print("*"*10)
        print(f"Handoff agent name: {agent_name}")
        print("*"*10)
    
    triage_agent = Agent(
        name="Manager Assistant",
        instructions = ("""
        You are a manager. You must never answer directly.
        If query is about LinkedIn → delegate to LinkedIn Assistant.
        If query is about WhatsApp → delegate to WhatsApp Assistant.
        """
        ),
        #model = LitellmModel(model=Model, api_key=gemini_key),
        #tools = [route_query],
         handoffs=[
            handoff(linkedin_agent, on_handoff=lambda ctx: on_handoff(linkedin_agent, ctx)),
            handoff(whatsapp_agent, on_handoff=lambda ctx: on_handoff(whatsapp_agent, ctx))
    ],
    )
    query = input("user query: ")
    result = await Runner.run(
        starting_agent = triage_agent,
        input = query,
        run_config = config
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    