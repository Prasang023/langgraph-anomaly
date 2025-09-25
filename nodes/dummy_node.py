from typing import Generic
from base_agent.states import BaseNodeStateTypeVar


class DummyStartingNode(Generic[BaseNodeStateTypeVar]):
    node_name = 'dummy_starting_node'

    async def execute(self, state: BaseNodeStateTypeVar, config):
        # Simple response that updates the state
        state["chat_history"] = state.get("chat_history", []) + ["Hello from dummy node!"]
        if state["session_store"].get("dummy_node"):
            state["session_store"]["dummy_node"].append("Hello from dummy node!")
        else:
            state["session_store"]["dummy_node"] = ["Hello from dummy node!"]

        return state
