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
    #Model = "gemini/gemini-2.0-flash"
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
    def post_on_linkedin() -> str:
        """Post content on LinkedIn"""
        return "Content successfully posted on LinkedIn"
    
    @function_tool
    def find_job_on_linkedin() -> str:
        """Search for remote frontend developer jobs on LinkedIn"""
        return "Searching for suitable frontend developer positions"
    
    @function_tool
    def route_query(query: str) -> str:
        """Route the query to appropriate assistant based on keywords"""
        if "linkedin" in query.lower():
            return handoff(
                agent=linkedin_agent,
                on_handoff=on_handoff
            )
        elif "whatsapp" in query.lower():
            return handoff(
                agent=whatsapp_agent,
                on_handoff=on_handoff
            )
        return "Sorry, I can't find a suitable assistant for your query."
    
    linkedin_agent = Agent(
        name="LinkedIn Assistant",
        instructions="""You are a LinkedIn assistant that helps with LinkedIn-specific tasks.
        Your responsibilities:
        1. Post content on LinkedIn when requested
        2. Search for remote frontend developer jobs
        Only handle LinkedIn-related queries and use the appropriate tools.""",
        tools=[post_on_linkedin, find_job_on_linkedin]
    )
    
    whatsapp_agent = Agent(
        name="WhatsApp Assistant",
        instructions="You are a WhatsApp assistant that handles WhatsApp-related queries and operations."
    )
    
    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]) -> None:
        """Callback function when handoff occurs"""
        print("=" * 40)
        print(f"Handoff to: {agent.name}")
        print("=" * 40)
    
    triage_agent = Agent(
        name="Manager Assistant",
        instructions="""You are a task routing manager.
        Your role is to analyze queries and delegate them to specialized assistants:
        - LinkedIn queries → LinkedIn Assistant
        - WhatsApp queries → WhatsApp Assistant
        Never answer queries directly, always delegate.""",
        tools=[route_query]
    )
    
    query = input("Please enter your query: ")
    result = await Runner.run(
        starting_agent = triage_agent,
        input = query,
        run_config = config
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    