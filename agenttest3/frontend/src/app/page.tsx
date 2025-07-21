"use client";

import { useState, useEffect } from 'react';
import { Agent, fetchAgents, createAgent, deleteAgent } from '@/lib/api-client';

export default function Home() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    instructions: '',
    output_type: 'str',
    description: ''
  });
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const agents = await fetchAgents();
      setAgents(agents);
      setError('');
    } catch (e) {
      setError('Failed to load agents');
      console.error(e);
    }
  };

  const handleCreateAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createAgent(newAgent);
      setShowCreateForm(false);
      setNewAgent({ name: '', instructions: '', output_type: 'str', description: '' });
      await loadAgents();
      setError('');
    } catch (e) {
      setError('Failed to create agent');
      console.error(e);
    }
  };

  const handleDeleteAgent = async (id: string) => {
    if (confirm('Are you sure you want to delete this agent?')) {
      try {
        await deleteAgent(id);
        await loadAgents();
        setError('');
      } catch (e) {
        setError('Failed to delete agent');
        console.error(e);
      }
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Agent Management</h1>
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Create New Agent
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {showCreateForm && (
          <div className="mb-8 p-4 border rounded">
            <h2 className="text-xl font-semibold mb-4">Create New Agent</h2>
            <form onSubmit={handleCreateAgent} className="space-y-4">
              <div>
                <label className="block mb-1">Name:</label>
                <input
                  type="text"
                  value={newAgent.name}
                  onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block mb-1">Instructions:</label>
                <textarea
                  value={newAgent.instructions}
                  onChange={(e) => setNewAgent({ ...newAgent, instructions: e.target.value })}
                  className="w-full p-2 border rounded"
                  rows={3}
                  required
                />
              </div>
              <div>
                <label className="block mb-1">Description:</label>
                <input
                  type="text"
                  value={newAgent.description}
                  onChange={(e) => setNewAgent({ ...newAgent, description: e.target.value })}
                  className="w-full p-2 border rounded"
                />
              </div>
              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Create Agent
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="grid gap-4">
          {agents.map((agent) => (
            <div key={agent.id} className="p-4 border rounded">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-semibold">{agent.name}</h3>
                  {agent.description && (
                    <p className="text-gray-600 mt-1">{agent.description}</p>
                  )}
                  <div className="mt-2">
                    <h4 className="font-medium">Instructions:</h4>
                    <p className="text-gray-700">{agent.instructions}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteAgent(agent.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
