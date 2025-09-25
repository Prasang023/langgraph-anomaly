import logging
import json
from typing import AsyncGenerator, Generic
from langgraph.graph.graph import CompiledGraph
from langchain_core.runnables.config import RunnableConfig

from base_agent.states import BaseNodeStateTypeVar


logger = logging.getLogger(__name__)


class LlmAgentExecutor(Generic[BaseNodeStateTypeVar]):
    def __init__(self, agent: CompiledGraph, agent_name: str):
        self.agent = agent
        self.agent_name = agent_name

    def prepare_response_meta(self, output):
        response_meta = {
            "request_tokens_used": output.get("request_tokens_used"),
            "response_tokens_used": output.get("response_tokens_used"),
        }

        return response_meta

    async def execute(self, initial_state: BaseNodeStateTypeVar) -> AsyncGenerator:
        logger.info(
            f"Executing agent: {self.agent_name} with initial state: {initial_state}"
        )
        
        # Simple execution without complex event streaming
        try:
            result = await self.agent.ainvoke(initial_state)
            logger.info(f"Agent execution completed with result: {result}")
            
            # Yield the chat history as streaming response
            chat_history = result.get("chat_history", [])
            for message in chat_history:
                yield f"{message}\n"
            
            # Yield completion marker
            response_meta = self.prepare_response_meta(result)
            yield f"\n{json.dumps(response_meta)}\n"
            yield "<end>"
            
        except Exception as e:
            logger.error(f"Error executing agent: {e}")
            yield f"Error: {str(e)}"
            yield "<end>"
