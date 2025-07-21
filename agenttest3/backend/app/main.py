from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import agents, chains

app = FastAPI(
    title="Agent Chain API",
    description="API for managing and executing agent chains",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # NextJS frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(chains.router, prefix="/api", tags=["chains"])

@app.get("/")
async def root():
    return {
        "message": "Agent Chain API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Import and register the existing agents from blogwriter.py
# This will populate the store with the default agents
from typing import List
from .models.agent import Agent, AgentCreate
from .store import store

def register_default_agents():
    default_agents: List[AgentCreate] = [
        AgentCreate(
            name="Search Agent",
            instructions="Search for information on the web about the given topic",
            output_type="str",
            description="Agent for web searching"
        ),
        AgentCreate(
            name="Outline Agent",
            instructions="Generate an outline based on the search results",
            output_type="str",
            description="Agent for creating content outlines"
        ),
        AgentCreate(
            name="Story Builder Agent",
            instructions="Generate a story based on the outline",
            output_type="str",
            description="Agent for creating story content"
        ),
        AgentCreate(
            name="Code Agent",
            instructions="Generate code snippets based on the story",
            output_type="str",
            description="Agent for generating code examples"
        ),
        AgentCreate(
            name="Review Agent",
            instructions="Review and provide feedback on the content",
            output_type="str",
            description="Agent for content review"
        )
    ]

    for agent_create in default_agents:
        store.create_agent(Agent(**agent_create.dict(), id="", input_agents=[]))

# Register default agents on startup
@app.on_event("startup")
async def startup_event():
    register_default_agents()
