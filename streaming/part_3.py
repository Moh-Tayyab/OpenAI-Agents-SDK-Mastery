# streaming/part_3.py
import asyncio, os
from dotenv import load_dotenv
from rich import print
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

@function_tool
async def burger_recommendation_tool(user_query: str) -> str:
    await asyncio.sleep(1)
    return "🍔 I recommend the classic cheeseburger at Burger Haven!"

@function_tool
async def payment_processing_tool(amount: float) -> str:
    await asyncio.sleep(1)
    return f"💳 Processed payment of ${amount:.2f} successfully."

async def main():
    client = AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = OpenAIChatCompletionsModel(model="gemini-1.5-flash", openai_client=client)
    config = RunConfig(model=model)

    agent = Agent(
        name="burger_agent",
        instructions="""You have two tools:
- burger_recommendation_tool → for burger suggestions
- payment_processing_tool → for payments
Always call them separately unless user explicitly asks for combined action.""",
        tools=[burger_recommendation_tool, payment_processing_tool],
    )

    query = input("user query: ")

    # Runner.run_streamed may be sync or async in different SDK versions.
    run_handle = Runner.run_streamed(starting_agent=agent, input=query, run_config=config)
    if asyncio.iscoroutine(run_handle):
        run_handle = await run_handle

    fallback_text = None
    inspected_first = False

    try:
        async for event in run_handle.stream_events():
            # (A) -- RAW token / LLM deltas (safe check)
            if hasattr(event, "data") and isinstance(event.data, ResponseTextDeltaEvent):
                # correct attribute: event.data.delta
                print(f"[cyan]{event.data.delta}[/cyan]", end="", flush=True)
                continue

            # (B) -- Run item / tool events (duck-typing)
            # Many SDKs expose .name/.item/.raw_item etc. Use attribute checks.
            if hasattr(event, "name") or hasattr(event, "item") or hasattr(event, "raw_item"):
                name = getattr(event, "name", "<no-name>")
                item = getattr(event, "item", getattr(event, "raw_item", None))
                print(f"\n[yellow]RunItem Event ({name})[/yellow]")
                # show concise info: tool name / type / output if present
                try:
                    if item is not None:
                        # some run items are dataclasses, some are dict-like
                        if hasattr(item, "__dict__"):
                            info = {k: v for k, v in item.__dict__.items() if k in ("name", "type", "output", "raw_item", "call_id")}
                            print(info)
                        else:
                            print(repr(item))
                except Exception:
                    print("Couldn't pretty-print item:", repr(item))

                # simple heuristic: tool output containing "Invalid JSON" or "error" -> fallback
                text_fields = str(item)
                if "Invalid JSON" in text_fields or "error" in text_fields.lower():
                    fallback_text = "Fallback → Sorry, the tool output was invalid. Please try again."
                    print(f"\n[⚠️ Tool Problem — streaming fallback]\n[DATA]: {fallback_text}")
                continue

            # (C) -- Agent update / handoff detection
            if hasattr(event, "new_agent"):
                print(f"\n[green]Agent Switch →[/green] {event.new_agent.name}")
                continue

            # (D) -- Unknown event: inspect once to confirm shape
            if not inspected_first:
                print("\n[debug] Unrecognized event (repr below). If you need to adapt, inspect this):")
                print(repr(event))
                inspected_first = True

    except Exception as exc:
        print(f"\n[red]Streaming loop raised an exception:[/red] {exc}")

    # override final output if we streamed a fallback
    if fallback_text:
        try:
            run_handle.final_output = fallback_text
        except Exception:
            # If final_output is read-only in this SDK version, just print fallback
            print("\n[bold magenta]Final Output (fallback):[/bold magenta]", fallback_text)
            return

    print(f"\n[bold magenta]Final Output: {run_handle.final_output}[/bold magenta]")


if __name__ == "__main__":
    asyncio.run(main())
