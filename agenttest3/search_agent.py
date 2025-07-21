from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings 

INSTRUCTIONS = (
    "You are a search agent.  Given a search term, you search the web for that term and"
    "produce a concise summary of the results around that topic. You can use the WebSearchTool"
    "to help you find relevant information."
    )

search_agent = Agent(
    name="Search Agent",     
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings = ModelSettings(tool_choice="required"),
    )
