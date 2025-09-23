
from agents import Agent, Runner,OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio, os
from rich import print

load_dotenv()

def main():
    API_KEy = os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
	
 
    AsyncOpenAI(
		api_key=API_KEy,
		base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
	
	)
	
    model = OpenAIChatCompletionsModel(
		model="gemini-1.5-flash",
		openai_client=AsyncOpenAI(
			api_key=API_KEy,
			base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
		)
	)
	
    config = RunConfig(
		model=model,
	)
    
    burger_agent = Agent(
		name = "burger_agent",
		instructions = """You are a friendly and knowledgeable assistant who ONLY helps users
			find the best burger places in town. Do not provide information about 
			any other fast food items like pizza, sandwiches, fries, or drinks. 
			If the user asks about anything other than burgers, politely remind 
			them that you specialize only in burgers.""",
		model=model
	)
    
    query = input("user query: ")
    try:
        result = Runner.run_sync(
			starting_agent = burger_agent,
			input = query,
			run_config = config,
			max_turns=0 # to disable agent interactions. this raise MaxTurnsExceeded exception
		)
        print(f"\n[bold yellow]Final Output: {result.final_output}[/bold yellow]")
    except Exception as e:
        print(f"⚠️ Excetion: [bold red]Error: {e}[/bold red]")
    
if __name__ == "__main__":
      main()   