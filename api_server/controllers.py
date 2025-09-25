from llm_agent.client import LlmAgentClient
from typing import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class ApiController:
    def __init__(self):
        self.llm_agent = LlmAgentClient()

    async def run_agent(
        self,
        query_id, 
        chat_type, 
        response_id, 
        agent_name_with_version,
    ) -> AsyncGenerator[str, None]:

        agent_response = self.llm_agent.process_query(
            query_id=query_id,
            response_id=response_id,
            agent_name_with_version=agent_name_with_version,
            chat_type=chat_type,
        )
        async for chunk in agent_response:
            yield chunk

    def run(self, query_id, chat_type, **kwargs):
        response_id = kwargs.get("response_id")
        agent_name_with_version = kwargs.get("agent_name_with_version")
        response = self.run_agent(
            query_id=query_id,
            chat_type=chat_type,
            response_id=response_id,
            agent_name_with_version=agent_name_with_version,
        )
        return response