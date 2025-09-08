from linkup import LinkupClient
from agents import function_tool, Agent, Runner
from datetime import datetime
import os
from dotenv import load_dotenv
from IPython.display import Markdown, display
import asyncio


load_dotenv()

async def main():
    #linkup_key= os.getenv("LINKUP_API_KEY")
    
    linkup_client=LinkupClient()
    @function_tool
    async def web_search() -> str:
        """Use this tool to search the web for information"""
    
    query=input("User's Query: ")
    response=await linkup_client.async_search(
        query=query,
        depth="standard",
        output_type="searchResults"
    )
    response
    
    answer = f"Search resuls for {query} on {datetime.now().strftime('%Y-%m-%d')}\n\n"
    for result in response.results[:3]:
        print(f"{result.name}\n{result.url}\n{result.content}\n\n")
        return answer
    
    web_search_agent = Agent(
        name = "Web Search Agent",
        model = "gpt-4.1-mini",
        instructions = ("You are a Web Search Agent that can search web for information. Once you have the required information, summerize it with cleanly formatted links sourcing each bit of information . Ensure you answer the question accurately and use markdown formatting"),
        tools = [web_search]
    )
    result = await Runner.run(
        starting_agent = web_search_agent,
        input=query,
    )
    display(Markdown(result.final_output))
if __name__ == "__main__":
    asyncio.run(main())    