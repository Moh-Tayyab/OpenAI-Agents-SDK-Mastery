from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.run import RunConfig
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config=RunConfig(
    model=model
) 

class Is_Medical_Query(BaseModel):
    is_medical_related: bool = Field(description="True if the query is related to medical topics, health, symptoms, treatments, medications, or healthcare. False if it's about other topics like sports, entertainment, technology, etc.")
    query_topic: str = Field(description="Brief description of what the query is about")

# Medical classification agent
medical_classifier_agent = Agent(  
    name="medical_classifier_agent",
    instructions="""You are a medical topic classifier for a patient medical assistant. Your job is to determine if a user's query is related to medical/healthcare topics or not.

IMPORTANT: You should be PERMISSIVE for medical-related or neutral queries, and only flag clearly NON-MEDICAL topics.

ALLOW these as medical/healthcare related:
- Health symptoms, conditions, diseases
- Medical treatments, procedures, medications
- Healthcare advice, diagnosis questions
- Medical equipment, terminology
- Mental health topics
- Nutrition and diet questions (all nutrition is health-related)
- Exercise and fitness questions (health-related)
- Basic greetings and conversational starters (hello, hi, how are you)
- General health inquiries
- Wellness and lifestyle questions
- Medical emergencies and first aid
- Preventive care questions

BLOCK only clearly non-medical topics:
- Sports events, matches, scores (not fitness/exercise)
- Entertainment (movies, music, celebrities)
- Technology (unless medical devices)
- Politics and current events
- Business and finance
- Travel planning
- Cooking recipes (unless for medical conditions)
- Academic subjects (unless medical education)

RULE: When in doubt, classify as medical-related. Only flag obvious non-medical topics.""",
    output_type=Is_Medical_Query,
    model=model
)

# Medical guardrail function
@input_guardrail
async def check_medical_topic(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    medical_result = await Runner.run(
        medical_classifier_agent,
        input,
        context=ctx
    )
    
    # Guardrail trips when query is NOT medical related
    # (i.e., when user talks about non-medical topics)
    non_medical_detected = not medical_result.final_output.is_medical_related
    
    return GuardrailFunctionOutput(
        output_info=medical_result.final_output,
        tripwire_triggered=non_medical_detected
    )

# Patient medical assistant agent
patient_agent = Agent(  
    name="Patient Medical Assistant",
    instructions="""You are a helpful medical assistant for patients. You can provide:
- General health information and education
- Explanation of medical terms and conditions  
- Information about symptoms and when to see a doctor
- Medication information and side effects
- Healthy lifestyle advice
- Mental health support and resources

Important disclaimers:
- Always remind patients to consult healthcare professionals for diagnosis
- Don't provide specific medical diagnoses
- Encourage seeking professional help for serious symptoms
- Provide accurate, evidence-based information only

You should only discuss medical and healthcare-related topics.""",
    input_guardrails=[check_medical_topic],
    model=model
)

async def main():
    print("=== Patient Medical Assistant ===")
    print("Main sirf medical aur healthcare topics ke baare mein baat kar sakta hun.")
    print("Agar aap koi aur topic ke baare mein puchenge to guardrail trigger ho jaayega.\n")
    
    while True:
        query = input("\nPatient query (or 'exit' to quit): ")
        
        if query.lower() == 'exit':
            print("Goodbye!")
            break
            
        try:
            result = await Runner.run(patient_agent, input=query, run_config=config)
            print("\n✅ Medical query detected - Response generated:")
            print(f"🤖 {result.final_output}")

        except InputGuardrailTripwireTriggered as e:
            print("\n🚨 GUARDRAIL TRIGGERED!")
            print("❌ Non-medical topic detected.")
            print(f"📊 Classification: {e.guardrail_result.output}")
            print("⚠️  Main sirf medical aur healthcare topics ke baare mein baat kar sakta hun.")
            print("💡 Kripaya koi medical ya health related question puchiye.")

if __name__ == "__main__":
    asyncio.run(main())