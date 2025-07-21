from agents import Agent

INSTRUCTIONS = (
    "You are a story builder agent. Your job is to generate a story based on the given input."
    "The story is for technical people to understand the concept in a simple way." 
    "Make sure to use the correct technical words and input code snippets where necessary."
    "The story should be creative and engaging."
    )


storybuilder_agent = Agent(
    name="Story Builder Agent",
    instructions=INSTRUCTIONS,
    output_type=str
    )
