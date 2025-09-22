# 🛠 Constructor Parameters (Roman Urdu Explanation)

# name: str
# → Agent ka naam. Ye ek string hoti hai. Example: "weather_agent"

# handoff_description: str | None
# → Human-readable description. Jab yeh agent kisi tool ya handoff ke andar use hoga to log samajh saken ke yeh agent kya karta hai.

# tools: list[Tool]
# → Tumhare agent ke pass kaunse tools available hain. Jaise calculator tool, weather API tool, database tool etc.

# instructions: str | Callable[...]
# → Yeh sab se important hai. Yeh basically tumhara system prompt hota hai jo agent ko batata hai uska role kya hai. Example: "You are a helpful weather assistant."

# prompt: Prompt | DynamicPromptFunction | None
# → Agar tum static ya dynamic prompt dena chaho (matlab har run pe change ho jaye), toh yeh idhar define hota hai.

# handoffs: list[Agent | Handoff]
# → Agar tum chahte ho ke yeh agent kuch kaam dusre agent ko forward kare (handoff kare), toh un agents ki list idhar hogi.

# model: str | Model | None
# → Konsa AI model use hoga. Example: "gpt-4o-mini" ya koi custom model object.

# model_settings: ModelSettings
# → Model ke settings (temperature, max tokens etc).

# input_guardrails: list[InputGuardrail]
# → Input par restrictions/validations lagane ke liye. Example: Agar user ghalat ya risky input de toh usko block kar do.

# output_guardrails: list[OutputGuardrail]
# → Output par restrictions/validations. Example: Agent kisi unsafe content ka jawab na de.

# output_type: type | AgentOutputSchemaBase | None
# → Tum specify kar sakte ho ke output kis type ka hona chahiye (JSON, custom schema, text etc).

# hooks: AgentHooks | None
# → Special events ke liye custom functions. Example: jab agent start ho ya jab tool use kare, us waqt kuch extra kaam karwana.

# tool_use_behavior
# → Ye decide karta hai ke tools kaise use honge:

# "run_llm_again" → Har tool ke baad LLM ko dobara chalana.

# "stop_on_first_tool" → Pehle tool use ke baad ruk jana.

# Custom function bhi de sakte ho.

# reset_tool_choice: bool
# → Agar True ho toh har run mein tool selection reset ho jata hai (agent fresh choice karega).

from agents import Agent, function_tool, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
import asyncio, os
import rich 

load_dotenv()

async def main():
    
    API_KEY=os.environ.get("GEMINI_API_KEY")
    OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

    model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

    config = RunConfig(
	 model=model
)
    # tool
    @function_tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers."""
        return a + b
    
    test_agent = Agent(
		name = "Test Agent", # this parameter is required
        instructions = "You are a helpful assistant.",
        tools = [add],
	)
    
    result = await Runner.run(
		starting_agent = test_agent,
		input = "what is the sum of 5 and 7?",
		run_config = config
  )
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    