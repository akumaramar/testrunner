from agents import Agent, Runner
# Use environment variable to set the API key
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Access the API key safely
# api_key = os.getenv("OPENAI_API_KEY")

# Console Output Hello
# print("Hello, World!")
# print("API Key:",
#      "Hidden" if not api_key or api_key == "your_api_key_here" else api_key)



# Check if API key is available
# if not api_key or api_key == "your_api_key_here":
#    raise ValueError("Please set a valid OPENAI_API_KEY in your .env file")

agent = Agent(name="Assistant", 
              instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.
