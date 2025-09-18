# modelsettings Presence_penalty and frequency_penalty, 

# frequency_penalty: 
# frequency_penalty → ek word ya phrase ko bar bar repeat karne pe penalty lagata hai.
# Matlab agar model “pizza pizza pizza” bolta hai, toh penalty is repetition ko kam karegi.

# Presence_penalty: presence_penalty → model ko naye topics introduce karne pe encourage karta hai.
# Matlab agar tum bolte ho “Tell me about pizza” aur presence_penalty zyada hai, toh model khud se aur naye related cheezen introduce karega jaise “pasta, burgers” bhi.

# Difference
# frequency_penalty = Stop spamming same words.
# presence_penalty = Bring new ideas into the conversation.

from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, StopAtTools, enable_verbose_stdout_logging
from dotenv import load_dotenv
from agents.run import RunConfig
from rich import print
import asyncio

import os

load_dotenv()

#enable_verbose_stdout_logging()


async def main():
	# gemini_api=os.getenv("GEMINI_API_KEY")
	# if not gemini_api:
	# 		raise ValueError("api key is not found.")
	# client=AsyncOpenAI(
	# 		api_key=gemini_api,
	# 		base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
	# )
		
	# model=OpenAIChatCompletionsModel(
	# 		model="gemini-2.0-flash",
	# 		openai_client=client
	# )
		
	# config=RunConfig(
	# 		model=model,
	# 		model_provider=client
	# )
	@function_tool
	def blog_writer(topic: str) -> str:
		"""
		Blog Writer Tool:
		- Takes a topic or keyword from the user.
		- Generates a detailed blog-style text with introduction, body, and conclusion.
		- Useful for creating articles, blog posts, or content drafts.
		"""
		return f"📝 Blog draft on '{topic}' created successfully."


	@function_tool
	def idea_creater(prompt: str) -> str:
		"""
		Idea Creator Tool:
		- Takes a short prompt or theme from the user.
		- Generates creative ideas, headlines, or outlines based on the prompt.
		- Useful for brainstorming, content planning, or topic suggestions.
		"""
		return f"💡 Here are some creative ideas for: '{prompt}'"
	agent = Agent(
		name ="Content Creator Agent",
		instructions = """
						You are a creative content assistant.
							- Use the blog_writer tool when the user asks to write a blog or article.
							- Use the idea_creater tool when the user needs brainstorming, topic ideas, or creative suggestions.
							- For other queries, answer directly without using tools.
						""",
		tools = [blog_writer, idea_creater],
		model_settings=ModelSettings(
			tool_choice="required",
			temperature=0.9,   # low randomness
            top_p=0.9,         # nucleus sampling
            frequency_penalty=1.0, # reduce repetition
            presence_penalty=1.2,  # encourage new ideas
            #include_usage=True,
            top_k=30       # restrict to top 50 tokens
		),
		#tool_use_behavior =StopAtTools(stop_at_tools_names= [])	
	)
 
 # Agar tum chahte ho ke empty input handle ho jaye, to simple check lagana hoga:
	query = input("user query: ").strip()
	if not query:
		query="⚠️ Please enter a valid query, empty input is not allowed."

	result = await Runner.run(
		starting_agent=agent,
		input=query,
		# run_config=config
		
	)
	print(result.final_output)

if __name__ == "__main__":
		asyncio.run(main())
		