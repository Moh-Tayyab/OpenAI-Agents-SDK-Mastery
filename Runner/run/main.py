# async version of Runner with Agent and OpenAI Agents SDK
from agents import Agent, Runner,OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, ModelSettings, enable_verbose_stdout_logging
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio, os
from rich import print

load_dotenv()
enable_verbose_stdout_logging()

async def main():
    # API_KEy = os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
	
 
    # AsyncOpenAI(
	# 	api_key=API_KEy,
	# 	base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
	
	# )
	
    # model = OpenAIChatCompletionsModel(
	# 	model="gemini-1.5-flash",
	# 	openai_client=AsyncOpenAI(
	# 		api_key=API_KEy,
	# 		base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	# 	)
	# )
	
    # config = RunConfig(
	# 	model=model,
	# )
    
    @function_tool
    async def burger_recommendation_tool(user_query: str) -> str:
        # Simulate an async operation, e.g., fetching from a database or API
        await asyncio.sleep(1)
		# For demonstration, return a static recommendation
        return "I recommend trying the classic cheeseburger at Burger Haven!"

    @function_tool
    async def pizza_recommendation_tool(user_query: str) -> str:
        await asyncio.sleep(1)
        return "I recommend trying the Margherita pizza at Pizza Palace!"

    @function_tool
    async def payment_processing_tool(amount: float) -> str:
        await asyncio.sleep(1)
        return f"Processed payment of ${amount:.2f} successfully."
	
    
    burger_agent = Agent(
        name="burger_agent",
        instructions=(
            "You help users find the best burger and pizza places. "
            "You must use the provided tools to answer any queries related to burgers, pizza, or payments. "
            "Do not answer such queries without calling the appropriate tool. "
            "If the query is unrelated to burgers, pizza, or payments, politely inform the user that you can only assist with those topics."
        ),
        tools=[burger_recommendation_tool, pizza_recommendation_tool, payment_processing_tool],
        model=OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=AsyncOpenAI(
                api_key=OPENAI_API_KEY,
            )
        ),
        model_settings=ModelSettings(
            parallel_tool_calls=True,
            tool_choice="required"
        )
    )
    
    query = input("user query: ")
    try:
        result = await Runner.run(
			starting_agent = burger_agent,
            input = query,
			#run_config = config,
			max_turns=2 # to disable agent interactions. this raise MaxTurnsExceeded exception
		)
        print(f"\n[bold purple]Final Output: {result.final_output}[/bold purple]")
    except Exception as e:
        print(f"⚠️ Excetion: [bold red]Error: {e}[/bold red]")
    
if __name__ == "__main__":
      asyncio.run(main())  