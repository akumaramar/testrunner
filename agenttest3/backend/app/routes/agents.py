from fastapi import APIRouter, HTTPException
from typing import List
from ..models.agent import Agent, AgentCreate, AgentUpdate, AgentExecution
from ..store import store

router = APIRouter()

@router.post("/agents/", response_model=Agent)
async def create_agent(agent: AgentCreate):
    new_agent = Agent(**agent.dict(), id="", input_agents=[])
    return store.create_agent(new_agent)

@router.get("/agents/", response_model=List[Agent])
async def list_agents():
    return store.list_agents()

@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    agent = store.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent: AgentUpdate):
    updated = store.update_agent(agent_id, Agent(**agent.dict(), id=agent_id))
    if updated is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return updated

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    if not store.delete_agent(agent_id):
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted"}

@router.post("/agents/{agent_id}/execute")
async def execute_agent(agent_id: str, execution: AgentExecution):
    agent = store.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    # TODO: Implement agent execution logic
    try:
        # For now, just return a mock response
        return {
            "agent_id": agent_id,
            "status": "completed",
            "output": f"Executed {agent.name} with input: {execution.input_data}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
