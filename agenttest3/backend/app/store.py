from typing import Dict, Optional, List
from .models.agent import Agent, AgentChain
import uuid

class InMemoryStore:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.chains: Dict[str, AgentChain] = {}

    def create_agent(self, agent: Agent) -> Agent:
        if not agent.id:
            agent.id = str(uuid.uuid4())
        self.agents[agent.id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def update_agent(self, agent_id: str, agent: Agent) -> Optional[Agent]:
        if agent_id in self.agents:
            agent.id = agent_id
            self.agents[agent_id] = agent
            return agent
        return None

    def delete_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

    def create_chain(self, chain: AgentChain) -> AgentChain:
        if not chain.id:
            chain.id = str(uuid.uuid4())
        self.chains[chain.id] = chain
        return chain

    def get_chain(self, chain_id: str) -> Optional[AgentChain]:
        return self.chains.get(chain_id)

    def list_chains(self) -> List[AgentChain]:
        return list(self.chains.values())

    def update_chain(self, chain_id: str, chain: AgentChain) -> Optional[AgentChain]:
        if chain_id in self.chains:
            chain.id = chain_id
            self.chains[chain_id] = chain
            return chain
        return None

    def delete_chain(self, chain_id: str) -> bool:
        if chain_id in self.chains:
            del self.chains[chain_id]
            return True
        return False

# Global store instance
store = InMemoryStore()
