export interface Agent {
  id: string;
  name: string;
  instructions: string;
  output_type: string;
  description?: string;
  parameters?: Record<string, any>;
  input_agents: string[];
}

export interface AgentChain {
  id: string;
  name: string;
  description?: string;
  agents: string[];
  connections: Record<string, string[]>;
}

const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchAgents(): Promise<Agent[]> {
  const response = await fetch(`${API_BASE_URL}/agents/`);
  if (!response.ok) throw new Error('Failed to fetch agents');
  return response.json();
}

export async function createAgent(agent: Omit<Agent, 'id' | 'input_agents'>): Promise<Agent> {
  const response = await fetch(`${API_BASE_URL}/agents/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error('Failed to create agent');
  return response.json();
}

export async function updateAgent(id: string, agent: Omit<Agent, 'id'>): Promise<Agent> {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(agent),
  });
  if (!response.ok) throw new Error('Failed to update agent');
  return response.json();
}

export async function deleteAgent(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/agents/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete agent');
}

export async function executeAgent(id: string, input: any): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/agents/${id}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input_data: input }),
  });
  if (!response.ok) throw new Error('Failed to execute agent');
  return response.json();
}

export async function fetchChains(): Promise<AgentChain[]> {
  const response = await fetch(`${API_BASE_URL}/chains/`);
  if (!response.ok) throw new Error('Failed to fetch chains');
  return response.json();
}

export async function createChain(chain: Omit<AgentChain, 'id'>): Promise<AgentChain> {
  const response = await fetch(`${API_BASE_URL}/chains/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(chain),
  });
  if (!response.ok) throw new Error('Failed to create chain');
  return response.json();
}

export async function updateChain(id: string, chain: Omit<AgentChain, 'id'>): Promise<AgentChain> {
  const response = await fetch(`${API_BASE_URL}/chains/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(chain),
  });
  if (!response.ok) throw new Error('Failed to update chain');
  return response.json();
}

export async function deleteChain(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chains/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) throw new Error('Failed to delete chain');
}

export async function executeChain(id: string, input: any): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/chains/${id}/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error('Failed to execute chain');
  return response.json();
}
