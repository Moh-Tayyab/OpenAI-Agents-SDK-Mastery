from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotent import load_dotenv
import os

load_dotenv()
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
    def geometeric_tool():
        description = "solve your query about geometeric related questions"
        
    @function_tool
    def algebra_tool():
        description = "solve your query about algebra related question"    
        
    math_agent = Agent(
        name = "math assistant",
        instructions = "Math helpful assistant. you are math teacher any user query simple, easy and straight forward way.",
        tools = [geometeric_tool, algebra_tool ]
    )
    bio_agent = Agent(
        name = "bio assistant",
        instructins = "you are Bio helpful assistant solve yours query about bio related or medical field. you have tools to use for better response",
        tools = []
    )
    student_agent = Agent(
        name = "",
        instructions = "",
        handoffs = []
    )
    result = await Runner.run(
        starting_agent = agent,
        input="hello",
        run_config = config
    )
    print(result.final_output)


if __name__ == "__main__":
    main()
