#!/usr/bin/env python3
"""
Simple command-line interface for running browser automations
"""

import asyncio
import json
import sys
import os
from main import run_generic_automation, TaskAutomation
from stagehand import StagehandConfig
from dotenv import load_dotenv

load_dotenv()

def load_config():
    """Load automation configuration"""
    try:
        with open('automation_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ automation_config.json not found!")
        return None

def list_scenarios(config):
    """List available automation scenarios"""
    print("📋 Available automation scenarios:")
    for key, scenario in config['scenarios'].items():
        print(f"  {key}: {scenario['name']}")
        print(f"    URL: {scenario['url']}")
        print(f"    Steps: {len(scenario['instructions'])}")
        print()

def run_scenario(scenario_name):
    """Run a specific scenario"""
    config = load_config()
    if not config:
        return
    
    if scenario_name not in config['scenarios']:
        print(f"❌ Scenario '{scenario_name}' not found!")
        list_scenarios(config)
        return
    
    scenario = config['scenarios'][scenario_name]
    print(f"🚀 Running: {scenario['name']}")
    print(f"🌐 URL: {scenario['url']}")
    print(f"📝 Instructions: {len(scenario['instructions'])} steps")
    print()
    
    # Run the automation
    asyncio.run(run_generic_automation(
        scenario['instructions'], 
        scenario['url']
    ))

def run_custom_automation(url, instructions):
    """Run custom automation with provided instructions"""
    print(f"🚀 Running custom automation")
    print(f"🌐 URL: {url}")
    print(f"📝 Instructions: {len(instructions)} steps")
    print()
    
    asyncio.run(run_generic_automation(instructions, url))

def interactive_mode():
    """Interactive mode to build automation step by step"""
    print("🎯 Interactive Automation Builder")
    print("Enter your instructions one by one. Type 'done' when finished.")
    print()
    
    url = input("Enter the website URL: ").strip()
    if not url:
        print("❌ URL is required!")
        return
    
    instructions = []
    print("\nEnter your automation instructions:")
    while True:
        instruction = input(f"Step {len(instructions) + 1}: ").strip()
        if instruction.lower() == 'done':
            break
        if instruction:
            instructions.append(instruction)
    
    if not instructions:
        print("❌ No instructions provided!")
        return
    
    print(f"\n📋 Your automation:")
    for i, instruction in enumerate(instructions, 1):
        print(f"  {i}. {instruction}")
    
    confirm = input("\nRun this automation? (y/n): ").strip().lower()
    if confirm == 'y':
        run_custom_automation(url, instructions)

def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print("🎯 Browser Automation Tool")
        print()
        print("Usage:")
        print("  python run_automation.py list                    - List available scenarios")
        print("  python run_automation.py run <scenario_name>     - Run a specific scenario")
        print("  python run_automation.py custom                  - Run custom automation")
        print("  python run_automation.py interactive             - Interactive mode")
        print()
        
        config = load_config()
        if config:
            list_scenarios(config)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        config = load_config()
        if config:
            list_scenarios(config)
    
    elif command == 'run':
        if len(sys.argv) < 3:
            print("❌ Please specify a scenario name!")
            print("Use 'python run_automation.py list' to see available scenarios")
            return
        scenario_name = sys.argv[2]
        run_scenario(scenario_name)
    
    elif command == 'custom':
        print("🎯 Custom Automation Mode")
        url = input("Enter website URL: ").strip()
        if not url:
            print("❌ URL is required!")
            return
        
        print("Enter instructions (one per line, empty line to finish):")
        instructions = []
        while True:
            instruction = input().strip()
            if not instruction:
                break
            instructions.append(instruction)
        
        if instructions:
            run_custom_automation(url, instructions)
        else:
            print("❌ No instructions provided!")
    
    elif command == 'interactive':
        interactive_mode()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'python run_automation.py' to see available commands")

if __name__ == "__main__":
    main() 