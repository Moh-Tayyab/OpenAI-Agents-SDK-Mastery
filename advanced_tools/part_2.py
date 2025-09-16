from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, MaxTurnsExceeded, ModelSettings
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    gemini_api = os.getenv("GEMINI_API_KEY")
    if not gemini_api:
        raise ValueError("api key is not found.")
    client = AsyncOpenAI(
        api_key=gemini_api,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )

    config = RunConfig(model=model, model_provider=client)

    @function_tool(is_enabled=True, name_override="weather")
    def fetch_weather() -> str:
        """Fetch the weather for a given location."""
        return "sunny"

    agent = Agent(
        name="weather assistant",
        instructions="you are helpful assistant help about weather",
        tools=[fetch_weather],
        model_settings=ModelSettings(tool_choice="required")
    )

    try:
        result = await Runner.run(
            starting_agent=agent,
            input="what is today weather in lahore",
            run_config=config,
            max_turns=2
        )
        print(result.new_items)
    except MaxTurnsExceeded as e:
        print(f"Max turns exceeded: {e}")

if __name__ == "__main__":
    asyncio.run(main())
