#!/usr/bin/env python3
"""
Simple test for browser-use authentication blocking
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Apply authentication blocking BEFORE importing browser-use
from utils.network_blocker import disable_cloud_environment
print("🔒 Applying authentication blocking...")
disable_cloud_environment()

# Check environment variables
print("\n📋 Environment Variables Set:")
browser_use_vars = [var for var in os.environ.keys() if var.startswith('BROWSER_USE_')]
for var in browser_use_vars:
    print(f"  {var} = {os.environ[var]}")

# Now import browser-use
try:
    from browser_use import Agent
    from browser_use.llm import ChatOpenAI
    print("\n✅ Browser-use imported successfully")
except Exception as e:
    print(f"\n❌ Failed to import browser-use: {e}")
    sys.exit(1)

async def test_simple_auth_block():
    """Test simple authentication blocking"""
    print("\n🧪 Testing Simple Authentication Blocking")
    print("=" * 40)
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Create ChatOpenAI instance
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )
        
        print("✅ LLM created successfully")
        
        # Create agent with minimal configuration
        agent = Agent(
            llm=llm,
            task="Go to https://example.com and get the page title",
            verbose=True,
            headless=True
        )
        
        print("✅ Agent created successfully")
        print("✅ Running agent...")
        
        # Run the agent
        result = await agent.run()
        
        print(f"✅ Agent completed successfully: {result}")
        print("✅ Authentication blocking is working!")
        
    except Exception as e:
        print(f"❌ Error during agent execution: {e}")
        if "auth" in str(e).lower() or "token" in str(e).lower():
            print("❌ Authentication blocking failed - still getting auth errors")
        else:
            print("⚠️  Error is not authentication-related")

if __name__ == "__main__":
    asyncio.run(test_simple_auth_block()) 