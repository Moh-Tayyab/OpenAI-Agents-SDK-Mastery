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
        """
        A tool for solving geometric problems including calculations and concepts related to
        shapes, angles, areas, volumes, and geometric transformations.
        Can handle 2D and 3D geometry questions.
        """
        
    @function_tool
    def algebra_tool():
        """
        A tool for solving algebraic problems including equations, expressions,
        polynomials, factoring, and graphing. Helps with both basic and
        advanced algebra concepts.
        """    
        
    @function_tool
    def cell_tool():
        """
        A specialized tool for answering questions about cell biology including
        cell structure, functions, organelles, cellular processes, and cell division.
        Covers both prokaryotic and eukaryotic cells.
        """
        
    @function_tool
    def vein_tool():
        """
        A tool for providing information about the circulatory system,
        specifically veins, arteries, and blood flow. Covers anatomy,
        functions, and common conditions related to veins.
        """
    math_agent = Agent(
        name = "math assistant",
        instructions = "Math helpful assistant. you are math teacher any user query simple, easy and straight forward way.",
        tools = [geometeric_tool, algebra_tool]
    )
    bio_agent = Agent(
        name = "bio assistant",
        instructins = "you are Bio helpful assistant solve yours query about bio related or medical field. you have tools to use for better response",
        tools = [cell_tool, vein_tool]
    )
    student_agent = Agent(
        name = "student assistant",
        instructions = "You are a helpful student assistant. For math questions, direct to the math assistant. For biology questions, direct to the bio assistant. Help students understand concepts clearly and simply.",
        handoffs = [math_agent, bio_agent]
    )
    query = input("user query: ")
    result = await Runner.run(
        starting_agent = student_agent,
        input=query,
        run_config = config
    )
    print(result.final_output)


if __name__ == "__main__":
    main()
