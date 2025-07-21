from fastapi import APIRouter, HTTPException
from typing import List
from ..models.agent import AgentChain
from ..store import store

router = APIRouter()

@router.post("/chains/", response_model=AgentChain)
async def create_chain(chain: AgentChain):
    return store.create_chain(chain)

@router.get("/chains/", response_model=List[AgentChain])
async def list_chains():
    return store.list_chains()

@router.get("/chains/{chain_id}", response_model=AgentChain)
async def get_chain(chain_id: str):
    chain = store.get_chain(chain_id)
    if chain is None:
        raise HTTPException(status_code=404, detail="Chain not found")
    return chain

@router.put("/chains/{chain_id}", response_model=AgentChain)
async def update_chain(chain_id: str, chain: AgentChain):
    updated = store.update_chain(chain_id, chain)
    if updated is None:
        raise HTTPException(status_code=404, detail="Chain not found")
    return updated

@router.delete("/chains/{chain_id}")
async def delete_chain(chain_id: str):
    if not store.delete_chain(chain_id):
        raise HTTPException(status_code=404, detail="Chain not found")
    return {"message": "Chain deleted"}

@router.post("/chains/{chain_id}/execute")
async def execute_chain(chain_id: str, input_data: dict):
    chain = store.get_chain(chain_id)
    if chain is None:
        raise HTTPException(status_code=404, detail="Chain not found")
    
    try:
        # TODO: Implement chain execution logic
        # For now, return a mock response
        results = []
        for agent_id in chain.agents:
            agent = store.get_agent(agent_id)
            if agent is None:
                raise HTTPException(status_code=404, detail=f"Agent {agent_id} in chain not found")
            results.append({
                "agent_id": agent_id,
                "agent_name": agent.name,
                "status": "completed",
                "output": f"Mock output from {agent.name}"
            })
        
        return {
            "chain_id": chain_id,
            "status": "completed",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
