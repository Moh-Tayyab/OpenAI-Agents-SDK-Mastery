

````markdown
## 🏃 Runner Examples

This repository now contains **both sync and async** implementations of `Runner` using the OpenAI Agents SDK.

---

### ✅ Sync Example
```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig

# Create Agent
burger_agent = Agent(
    name="burger_agent",
    instructions="You help users find the best burger places in town.",
    model=OpenAIChatCompletionsModel(
        model="gpt-4o-mini",
        openai_client=AsyncOpenAI(api_key="YOUR_API_KEY")
    )
)

query = "Suggest me a good burger place."

# Run synchronously
result = Runner.run(
    starting_agent=burger_agent,
    input=query
)
print("Final Output:", result.final_output)
````

---

### ⚡ Async Example with Parallel Tool Calls

```python
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, ModelSettings

# Define async tools
@function_tool
async def burger_recommendation_tool(user_query: str) -> str:
    return "Try the classic cheeseburger at Burger Haven!"

@function_tool
async def pizza_recommendation_tool(user_query: str) -> str:
    return "Try the Margherita pizza at Pizza Palace!"

@function_tool
async def payment_processing_tool(amount: float) -> str:
    return f"Processed payment of ${amount:.2f} successfully."

async def main():
    burger_agent = Agent(
        name="burger_agent",
        instructions="You help users find the best burger and pizza places.",
        tools=[burger_recommendation_tool, pizza_recommendation_tool, payment_processing_tool],
        model=OpenAIChatCompletionsModel(
            model="gpt-4o-mini",
            openai_client=AsyncOpenAI(api_key="YOUR_API_KEY")
        ),
        model_settings=ModelSettings(
            parallel_tool_calls=True,
            tool_choice="required"
        )
    )

    query = "Suggest a burger, a pizza, and process a $12.75 payment."

    result = await Runner.run(
        starting_agent=burger_agent,
        input=query,
        max_turns=2  # allow extra turn for final response
    )
    print("Final Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 📝 


