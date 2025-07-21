from agents import Agent

INSTRUCTIONS = (
    "You are a code generation agent. Your job is to generate code snippets based the toppics given to you."
    "The generated code should have all the necessary imports and should be ready to run."
    "You can use the CodeGenerationTool to help you generate code snippets."
    )

code_agent = Agent(
    name="Code Agent",
    instructions=INSTRUCTIONS,
    output_type=str
    )