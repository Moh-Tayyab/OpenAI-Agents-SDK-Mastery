#Customizing handoffs via the handoff() function
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff
from dotenv import load_dotenv
#from agents.run import RunConfig
from agents.extensions.models.litellm_model import LitellmModel
import os 
import asyncio
#from agents import enable_verbose_stdout_logging

load_dotenv()

#enable_verbose_stdout_logging()
#set_tracing_disable(dissble=True)


async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    Model = "gemini/gemini-2.0-flash"
    # if not gemini_key:
    #     raise ValueError("api key not found.")
    
    # client=AsyncOpenAI(
    #     api_key=gemini_key,
    #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    # )
    # model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
   
    # config = RunConfig(
    #     model=model
    # )
    
    @function_tool
    def route_query(query):
        if "linkedin" in query.lower():
        #yh aider custom handoff ka concept use ho rha hai
          return handoff(name = "LinkedIn Post Assistant", instructions = "You are a helpfull assitant that help to post content on linkedin.")
        elif "whatsapp" in query.lower():
            return handoff(name = "Whatsapp Assistant", instructions = "You are a helpfull assistant to handle my personal whatsapp",)
        else:
            return "I can’t find a suitable assistant."
        
    # linkedin_agent = Agent(
    #     name = "LinkedIn Post Assistant",
    #     instructions = "You are a helpfull assitant that help to post content on linkedin.",
    #     model=model
        
    # )
    
    # whatsapp_agent = Agent(
    #     name = "Whatsapp Assistant",
    #     instructions = "You are a helpfull assistant to handle my personal whatsapp",
    #     model=model
    #)
    
    main_agent = Agent(
        name="Manager Assistant",
        instructions = "you can help user smoothly and deliery user query to specialist Assistant.",
        #model=model,
        model = LitellmModel(model=Model, api_key=gemini_key),
        tools = [route_query]
    )
    query = input("user query: ")
    result = await Runner.run(
        starting_agent = main_agent,
        input= query,
        #run_config = config
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    