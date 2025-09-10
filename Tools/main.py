from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

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
        return "Geometric tool was called"
        
    @function_tool
    def algebra_tool():
        """
        A tool for solving algebraic problems including equations, expressions,
        polynomials, factoring, and graphing. Helps with both basic and
        advanced algebra concepts.
        """    
        return "Algebra tool was called"
        
    @function_tool(name_override="cell")
    def cell_tool():
        """
        A specialized tool for analyzing and comparing different cell types, structures,
        and functions. Can explain differences between cells like red blood cells,
        white blood cells, and other cell types. Covers cell biology including
        cell structure, functions, organelles, and cellular processes.
        """
        return "Cell biology tool was called"
        
    @function_tool
    def vein_tool():
        """
        A tool for providing information about the circulatory system,
        specifically veins, arteries, and blood flow. Covers anatomy,
        functions, and common conditions related to veins.
        """
        return "Vein/circulatory tool was called"

    math_agent = Agent(
        name = "math assistant",
        instructions = "Math helpful assistant. You are a math teacher. Use the geometric_tool for geometry questions and algebra_tool for algebra questions.",
        tools = [geometeric_tool, algebra_tool]
    )
    bio_agent = Agent(
        name = "bio assistant",
        instructions = "You are a biology assistant. Use the cell_tool for questions about cell types, structures, and comparisons between different cells. Use the vein_tool for questions about the circulatory system.",
        tools = [cell_tool, vein_tool]
    )
    student_agent = Agent(
        name = "student assistant",
        instructions = "You are a helpful student assistant. For math questions, direct to the math assistant. For biology questions like cells, cell comparisons, or circulation, direct to the bio assistant.",
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
    asyncio.run(main())
