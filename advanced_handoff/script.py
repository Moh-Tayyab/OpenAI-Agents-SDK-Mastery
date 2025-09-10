#Customizing via handoff() function
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper
from dotenv import load_dotenv
from agents.run import RunConfig
#from agents.extensions.models.litellm_model import LitellmModel
#from agents.extensions.visualization import draw_graph
import os 
import asyncio
#from agents import enable_verbose_stdout_logging

load_dotenv()

#enable_verbose_stdout_logging()
#set_tracing_disable(dissble=True)


async def main():
    gemini_key = os.getenv("GEMINI_API_KEY")

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
    
    @function_tool
    def routequery(q):
        if "openai" in q:
            return handoff(
				agent=openAI_agent,
			)
        elif "devops" in q:
            return handoff(
				agent=devops_agent
			)   
            
             
    web_dev_agent = Agent(
        name = "Web Developer",
        instructions = "",
	)
    mobile_dev_agent = Agent(
        name = "Mobile Developer",
        instructions = "",
	)
    agenticAI_agent = Agent(
        name = "Agentic AI Developer",
        instructions = "",
        tools = [routequery]
	)
    devops_agent = Agent(
        name = "Devops Agent",
        instructions = ""
	)
    openAI_agent = Agent(
        name = "OpenAI Agent",
        instructions = ""
	)
    panacloud_agent = Agent(
        name = "Panacloud",
        instructions = "",
        handoffs = [web_dev_agent, mobile_dev_agent, agenticAI_agent]
	)
    
    
    query = input("user query: ")
    result = await Runner.run(
        starting_agent = panacloud_agent,
        input = query,
        run_config = config
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    