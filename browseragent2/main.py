import asyncio
import os
from stagehand import Stagehand, StagehandConfig
from dotenv import load_dotenv
import json
from typing import List, Dict, Any

load_dotenv()

class TaskAutomation:
    def __init__(self, config: StagehandConfig):
        self.config = config
        self.stagehand = None
        self.page = None
        self.context = {}
        
    async def init(self):
        """Initialize the automation system"""
        self.stagehand = Stagehand(self.config)
        await self.stagehand.init()
        self.page = self.stagehand.page
        
    async def close(self):
        """Clean up resources"""
        if self.stagehand:
            await self.stagehand.close()
            
    async def analyze_page(self, description: str = "Analyze the current page state") -> str:
        """Analyze the current page and return a description"""
        result = await self.page.extract(description)
        return result.extraction
        
    async def execute_instruction(self, instruction: str, max_retries: int = 3) -> Dict[str, Any]:
        """Execute a high-level instruction with automatic retry and verification"""
        print(f"🎯 Executing: {instruction}")
        
        for attempt in range(max_retries):
            try:
                print(f"📋 Attempt {attempt + 1}/{max_retries}")
                
                # Execute the instruction
                await self.page.act(instruction)
                await asyncio.sleep(2)
                
                # Verify the result
                verification = await self.verify_instruction_result(instruction)
                
                if verification['success']:
                    print(f"✅ Instruction completed successfully: {verification['summary']}")
                    return {
                        'success': True,
                        'attempt': attempt + 1,
                        'result': verification['summary'],
                        'context': verification['context']
                    }
                else:
                    print(f"⚠️ Instruction may not have completed as expected: {verification['summary']}")
                    if attempt < max_retries - 1:
                        print("🔄 Retrying with more specific approach...")
                        # Try a more detailed approach
                        detailed_instruction = await self.generate_detailed_instruction(instruction, verification['context'])
                        await self.page.act(detailed_instruction)
                        await asyncio.sleep(2)
                        
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    
        return {
            'success': False,
            'attempts': max_retries,
            'result': f"Failed to execute: {instruction}"
        }
    
    async def verify_instruction_result(self, instruction: str) -> Dict[str, Any]:
        """Verify if an instruction was executed successfully"""
        # Ask the AI to verify the result
        verification_prompt = f"""
        I just executed this instruction: "{instruction}"
        
        Please analyze the current page state and tell me:
        1. Was the instruction completed successfully?
        2. What is the current state of the page?
        3. What should I do next?
        
        Respond with a clear assessment of success/failure and current context.
        """
        
        result = await self.page.extract(verification_prompt)
        context = result.extraction
        
        # Simple success detection
        success_indicators = ['success', 'completed', 'done', 'finished', 'achieved']
        failure_indicators = ['error', 'failed', 'not found', 'cannot', 'unable']
        
        text_lower = context.lower()
        success = any(indicator in text_lower for indicator in success_indicators)
        failure = any(indicator in text_lower for indicator in failure_indicators)
        
        return {
            'success': success and not failure,
            'summary': context,
            'context': context
        }
    
    async def generate_detailed_instruction(self, original_instruction: str, context: str) -> str:
        """Generate a more detailed instruction based on context"""
        detailed_prompt = f"""
        The original instruction was: "{original_instruction}"
        Current context: {context}
        
        Please provide a more detailed, step-by-step instruction that will accomplish the same goal.
        Be very specific about what elements to find and what actions to take.
        """
        
        result = await self.page.extract(detailed_prompt)
        return result.extraction
    
    async def run_automation_sequence(self, instructions: List[str]) -> List[Dict[str, Any]]:
        """Run a sequence of automation instructions"""
        results = []
        
        for i, instruction in enumerate(instructions, 1):
            print(f"\n🔄 Step {i}/{len(instructions)}")
            result = await self.execute_instruction(instruction)
            results.append(result)
            
            if not result['success']:
                print(f"❌ Step {i} failed, stopping sequence")
                break
                
            # Update context for next steps
            self.context[f'step_{i}_result'] = result['result']
            
        return results
    
    async def smart_login(self, username: str = "user", password: str = "pass") -> bool:
        """Smart login that adapts to different login forms"""
        print("🔐 Starting smart login process...")
        
        # Analyze the login page
        page_analysis = await self.analyze_page("Describe the login form and available elements")
        print(f"📄 Page analysis: {page_analysis}")
        
        # Try intelligent login
        login_instruction = f"""
        Perform a complete login process:
        1. Find the username/email input field and enter '{username}'
        2. Find the password input field and enter '{password}'
        3. Submit the form by clicking the login/submit button or pressing Enter
        4. Wait for the page to load and verify login success
        """
        
        result = await self.execute_instruction(login_instruction)
        
        if result['success']:
            # Verify login status
            verification = await self.analyze_page("Am I successfully logged in? What do I see on the page?")
            if any(indicator in verification.lower() for indicator in ['dashboard', 'welcome', 'logged in', 'success']):
                print("✅ Login verified successfully!")
                return True
        
        print("❌ Login failed")
        return False

async def run_generic_automation(instructions: List[str], url: str = "https://v0-small-task-manager-app.vercel.app/"):
    """Generic automation runner that can handle any set of instructions"""
    
    config = StagehandConfig(
        env="LOCAL",
        model_name="openai/gpt-4.1-mini",
        model_client_options={"apiKey": os.getenv("MODEL_API_KEY")},
        log_inference_to_file=True,
        verbose=True,
    )
    
    automation = TaskAutomation(config)
    
    try:
        await automation.init()
        
        print("🚀 Starting generic automation...")
        
        # Navigate to the target URL
        print(f"🌐 Navigating to: {url}")
        await automation.page.goto(url)
        await automation.page.wait_for_load_state("networkidle")
        
        # Run the automation sequence
        results = await automation.run_automation_sequence(instructions)
        
        # Print summary
        print("\n📊 Automation Summary:")
        for i, result in enumerate(results, 1):
            status = "✅ Success" if result['success'] else "❌ Failed"
            print(f"Step {i}: {status}")
            if result['success']:
                print(f"   Result: {result['result'][:100]}...")
        
        return results
        
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return []
    finally:
        await automation.close()

# Example usage functions
async def example_task_manager_automation():
    """Example: Complete task manager automation"""
    instructions = [
        "Login to the application using username 'user' and password 'pass'",
        "Create a new task with title 'Complete automation project' and description 'Finish the browser automation system'",
        "Mark the task as completed",
        "Logout from the application"
    ]
    
    return await run_generic_automation(instructions)

async def example_ecommerce_automation():
    """Example: E-commerce automation"""
    instructions = [
        "Navigate to the products page",
        "Search for 'laptop'",
        "Add the first laptop to cart",
        "Proceed to checkout",
        "Fill in shipping information",
        "Complete the purchase"
    ]
    
    return await run_generic_automation(instructions, "https://example-ecommerce.com")

async def custom_automation(instructions: List[str], url: str):
    """Run custom automation with your own instructions"""
    return await run_generic_automation(instructions, url)

async def main():
    """Main function - choose your automation scenario"""
    
    # Option 1: Run the task manager example
    print("🎯 Running Task Manager Automation Example")
    await example_task_manager_automation()
    
    # Option 2: Run custom automation
    # custom_instructions = [
    #     "Your custom instruction 1",
    #     "Your custom instruction 2",
    #     "Your custom instruction 3"
    # ]
    # await custom_automation(custom_instructions, "https://your-website.com")
    
    # Option 3: Interactive mode
    # instructions = []
    # while True:
    #     instruction = input("Enter instruction (or 'done' to finish): ")
    #     if instruction.lower() == 'done':
    #         break
    #     instructions.append(instruction)
    # await custom_automation(instructions, "https://your-website.com")

if __name__ == "__main__":
    asyncio.run(main())