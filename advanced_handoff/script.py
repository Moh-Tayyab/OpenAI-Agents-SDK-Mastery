
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
    
    def on_handoff(ctx: RunContextWrapper):
        #agent_name = agent.name
        print("-"*10)
        print(f"Handoff agent name: {ctx.agent.name}")
        print("-"*10)
        
    @function_tool
    def routequery(q: str) -> handoff:
        """Route the query to appropriate specialized agent"""
        q = q.lower()  # Convert to lowercase for better matching
        
        if "openai" in q:
            return handoff(
                agent=openAI_agent,
                on_handoff=on_handoff
            )
        elif "devops" in q:
            return handoff(
                agent=devops_agent,
                on_handoff=on_handoff
            )
        return None  # Handle case when no matching condition is found
            
    web_dev_agent = Agent(
        name = "Web Developer",
        instructions = "I am a professional web developer specializing in modern web technologies, frameworks, and best practices. I can help with frontend, backend, and full-stack development questions.",
        )
    mobile_dev_agent = Agent(
        name = "Mobile Developer",
        instructions = "I specialize in mobile app development for iOS and Android platforms, using native and cross-platform frameworks. I can assist with mobile architecture, UI/UX, and performance optimization.",
        )
    agenticAI_agent = Agent(
        name = "Agentic AI Developer",
        instructions = """
        You are an AI specialist focused on autonomous AI agents.
        For handling specific domain queries:
        - If the query mentions OpenAI → call the `routequery` tool to handoff to OpenAI Agent.
        - If the query mentions DevOps → call the `routequery` tool to handoff to DevOps Agent.
        Always use the routequery tool for routing instead of answering directly.
        """,
tools = [routequery]
        )
    devops_agent = Agent(
        name = "Devops Agent",
        instructions = "I specialize in DevOps practices including CI/CD, containerization, cloud infrastructure, and automation. I can help with deployment, scaling, and infrastructure management."
        )
    openAI_agent = Agent(
        name = "OpenAI Agent",
        instructions = "I am specialized in OpenAI's technologies and APIs. I can assist with integrating and optimizing OpenAI services, including GPT models and DALL-E."
        )
    panacloud_agent = Agent(
        name = "Panacloud",
        instructions = "I am your primary agent for coordinating development queries. I can direct you to specialized agents for web, mobile, or AI development based on your needs.",
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