from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
import json
from datetime import datetime
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config = RunConfig(
    model=model
)

class ConversationSummary(BaseModel):
    important_information: str = Field(description="Key insights, important points, or critical information discussed")
    current_date: str = Field(description="Current date in DD/MM/YYYY format")
    current_time: str = Field(description="Current time in HH:MM AM/PM format")  
    summary: str = Field(description="Engaging and comprehensive conversation summary that captures the essence, flow, and key outcomes in a natural, interesting way that keeps the reader engaged")

# Professional summary agent
summary_agent = Agent(
    name="Professional Conversation Summary Assistant",
    instructions=f"""You are a professional conversation summary specialist who creates engaging, comprehensive, and naturally flowing summaries that people actually want to read.

CORE APPROACH:
- Write summaries that flow like a story, not bullet points
- Make it engaging and interesting, not boring or mechanical  
- Capture the conversation's personality and tone
- Include relevant context and background when helpful
- Write in a way that keeps the reader interested throughout

SUMMARY STYLE:
- Start with the most interesting or important aspect
- Use natural, conversational language
- Include specific details that matter
- Show the progression and flow of the conversation
- End with outcomes, decisions, or next steps if applicable
- Make it comprehensive yet digestible
- Focus on what the reader needs to know and would find valuable

AVOID:
- Robotic, templated language
- Unnecessary word limits that make summaries feel chopped
- Generic phrases like "the conversation covered" or "topics discussed included"
- Boring, clinical tone
- Excessive brevity that loses important context

IMPORTANT INFORMATION SECTION:
- Extract the most crucial points, decisions, or insights
- Include actionable items, key facts, or critical details
- Make it comprehensive enough to be truly useful

CURRENT CONTEXT:
- Today's date: {datetime.now().strftime('%d/%m/%Y')}
- Current time: {datetime.now().strftime('%I:%M %p')}

Create summaries that people actually want to read and find genuinely helpful.""",
    output_type=ConversationSummary,
    model=model
)

async def main():
    print("=== Professional Conversation Summary Agent ===")
    print("Main kisi bhi conversation ka professional summary bana sakta hun.\n")
    
    while True:
        print("\nOptions:")
        print("1. Enter conversation text for summary")
        print("2. Type 'exit' to quit")
        
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() == 'exit':
            print("Goodbye!")
            break
            
        if choice == '1' or choice.lower() not in ['exit']:
            print("\nPlease enter the conversation text (press Enter twice when done):")
            conversation_lines = []
            empty_line_count = 0
            
            while True:
                line = input()
                if line == "":
                    empty_line_count += 1
                    if empty_line_count >= 2:
                        break
                
                    empty_line_count = 0
                    conversation_lines.append(line)
            
            if not conversation_lines:
                print("❌ No conversation text provided.")
                continue
                
            conversation_text = "\n".join(conversation_lines)
            
            print("\n📋 Generating professional summary...")
            try:
                summary_result = await Runner.run(
                    summary_agent, 
                    input=f"Analyze this conversation and provide a structured professional summary:\n\n{conversation_text}",
                    run_config=config
                )
                
                # Create JSON output
                summary_json = {
                    "date": summary_result.final_output.current_date,
                    "time": summary_result.final_output.current_time,
                    "important_information": summary_result.final_output.important_information,
                    "summary": summary_result.final_output.summary
                }
                
                print("\n" + "="*60)
                print("📊 CONVERSATION SUMMARY (JSON FORMAT)")
                print("="*60)
                print(json.dumps(summary_json, indent=2, ensure_ascii=False))
                print("="*60)
                
            except Exception as e:
                print(f"❌ Error generating summary: {e}")

if __name__ == "__main__":
    asyncio.run(main())