from threading import Lock
from typing import Dict, Type, List
from base_agent.base import BaseAgent


class LlmAgentFactory:
    _instance = None  # Singleton instance
    _lock = Lock()  # Lock for thread safety

    def __init__(self, available_agents: List[Type[BaseAgent]]):
        if not hasattr(self, "_initialized"):  # Ensure initialization only happens once
            self._agents: dict[str, Type[BaseAgent]] = {}
            self._agent_map: Dict[str, Type[BaseAgent]] = {
                agent.agent_name: agent for agent in available_agents
            }
            self._initialized = True

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    @classmethod
    def initialize(cls, available_agents: List[Type[BaseAgent]]):
        """
        Initializes the factory with the provided available agents.
        """
        return cls(available_agents)

    @classmethod
    def get_agent(cls, agent_name: str):
        """
        Retrieves an agent by its name. If it is not already initialized,
        it creates and stores it in the cache.
        """
        instance = cls._instance
        if instance is None:
            raise Exception(agent_name)

        # Return cached agent if it exists
        if agent_name in instance._agents:
            return instance._agents[agent_name]

        # Check if the agent name exists in the map
        if agent_name not in instance._agent_map:
            raise Exception(agent_name)

        # Create and cache the agent
        agent_class = instance._agent_map[agent_name]
        instance._agents[agent_name] = agent_class.get_compiled_agent()
        return instance._agents[agent_name]
