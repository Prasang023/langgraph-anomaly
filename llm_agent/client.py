from typing import AsyncGenerator
from base_agent.base import BaseAgent
from base_agent.factory import LlmAgentFactory
from base_agent.states import BaseNodeState
from base_agent.controller import LlmAgentController
from langgraph.graph import StateGraph, END
from nodes.dummy_node import DummyStartingNode
import logging

logger = logging.getLogger(__name__)


class OpenLoopAgentV1(BaseAgent[BaseNodeState]):
    agent_name = "open_loop_agent_v1"
    state = BaseNodeState

    @classmethod
    def create_agent_graph(cls, flow: StateGraph):
        flow.add_node('dummy_starting_node', DummyStartingNode().execute)
        flow.set_entry_point('dummy_starting_node')
        flow.add_edge('dummy_starting_node', END)


LlmAgentFactory.initialize(
    [
        OpenLoopAgentV1,
    ]
)


class LlmAgentClient:
    def process_query(
        self,
        query_id,
        response_id,
        agent_name_with_version,
        chat_type,
        chat_history=[],
        session_store={},
    ) -> AsyncGenerator[str, None]:
        try:
            logger.info(f"Check session store value here: {session_store}")
            logger.info(f"Check chat history value here: {chat_history}")
            logger.info("Why is session store value persisting from previous request?")
            logger.info("How is this session store variable from langgraph state accessible here globally?")
            logger.info("How is this session store variable from langgraph state overriding the session store default value declared in function signature?")
            logger.info("Why is chat history not behaving like session store?")
            initial_state: BaseNodeState = {
                # Base Node state keys
                "response_id": response_id,
                "agent_name": agent_name_with_version,
                "chat_history": chat_history,
                "data_required": [],
                "user_data": {},
                "user_data_meta": {},
                "request_tokens_used": 0,
                "response_tokens_used": 0,
                "chat_type": chat_type,
                "session_store": session_store,
            }

            return LlmAgentController[BaseNodeState]().process_query(
                agent_name_with_version, initial_state
            )

        except Exception as e:
            print(
                f"Error processing in LLM Agent Controller query id: {query_id} response id: {response_id} agent name: {agent_name_with_version} error: {e}",
            )
