from agent import Agent, Runner, PGuardrails

async def main():
    agent = Agent(
        name = "Guardrails",
        instructions = "You are a helpful assistant that follows guardrails.",
        model = "gpt-4o-mini",
        guardrail = Guardrails()
    )
    
    result = await Runner.run(
        starting_agent = agent,
        input = "Hello, how are you?"
        
    )
    print("Hello from guardarails!")


if __name__ == "__main__":
    main()
