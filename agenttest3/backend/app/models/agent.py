from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class AgentBase(BaseModel):
    name: str
    instructions: str
    output_type: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Agent(AgentBase):
    id: str
    input_agents: List[str] = Field(default_factory=list)  # IDs of agents that feed into this agent

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    pass

class AgentExecution(BaseModel):
    agent_id: str
    input_data: Any
    execution_context: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AgentChain(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    agents: List[str]  # List of agent IDs in execution order
    connections: Dict[str, List[str]]  # Map of agent ID to list of next agent IDs
