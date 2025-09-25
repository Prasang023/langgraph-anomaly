from typing import Generic, Type, AsyncGenerator

from base_agent.executor import LlmAgentExecutor
from base_agent.factory import LlmAgentFactory
from base_agent.states import BaseNodeStateTypeVar


class LlmAgentController(Generic[BaseNodeStateTypeVar]):
    def process_query(
        self, agent_name: str, initial_state: BaseNodeStateTypeVar
    ) -> AsyncGenerator[str, None]:
        response_id = initial_state.get("response_id") or ""

        try:
            agent = LlmAgentFactory.get_agent(agent_name)

            try:
                executor = LlmAgentExecutor[BaseNodeStateTypeVar](agent, agent_name)
                response = executor.execute(initial_state)

                return response
            except Exception as e:
                print(
                    f"Error while streaming response id: {response_id} agent name: {agent_name} error: {e}",
                )

        except Exception as e:
            raise e
