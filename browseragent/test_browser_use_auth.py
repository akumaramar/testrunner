#!/usr/bin/env python3
"""
Test browser-use agent with authentication log suppression
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Apply authentication suppression before importing browser-use
from utils.network_blocker import disable_cloud_environment
disable_cloud_environment()

# Now import browser-use
from browser_use import Agent
from browser_use.llm import ChatOpenAI

async def test_browser_use_auth_suppression():
    """Test browser-use agent with suppressed authentication logs"""
    print("Testing Browser-Use Agent with Authentication Suppression")
    print("=" * 60)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Create ChatOpenAI instance
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        
        # Create agent with minimal configuration
        agent = Agent(
            llm=llm,
            task="Go to https://example.com and get the page title",
            verbose=True,
            headless=True
        )
        
        print("✅ Agent created successfully")
        print("✅ Authentication logs should be suppressed")
        print("✅ Running agent...")
        
        # Run the agent
        result = await agent.run()
        
        print(f"✅ Agent completed: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_browser_use_auth_suppression()) 