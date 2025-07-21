import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from browser_use.llm import ChatOpenAI

async def main():
    print("Hello from browseragent!")

    agent = Agent(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        verbose=True,
        task="search for the best north indian restaurant in bangalore",
    )

    result = await agent.run()
    print(result)


# Add Main function here
if __name__ == "__main__":
    asyncio.run(main())


    
