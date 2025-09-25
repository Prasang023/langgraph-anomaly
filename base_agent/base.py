import os
from typing import Generic, Type
from langgraph.graph import StateGraph
from decouple import config

from base_agent.constants import BASE_AGENT_V1
from base_agent.states import BaseNodeState, BaseNodeStateTypeVar

curr_dir = os.getcwd()


class BaseAgent(Generic[BaseNodeStateTypeVar]):
    agent_name = BASE_AGENT_V1
    state: Type[BaseNodeStateTypeVar] | None = None

    @classmethod
    def create_agent_graph(cls, flow: StateGraph):
        pass

    @classmethod
    def get_compiled_agent(cls, config_schema=None):
        if cls.state is None:
            raise Exception("State not set")

        required_keys = BaseNodeState.__annotations__.keys()
        if not all(key in cls.state.__annotations__.keys() for key in required_keys):
            raise TypeError("State does not match BaseNodeState structure")

        flow = StateGraph(cls.state, config_schema=config_schema)

        cls.create_agent_graph(flow)

        compiled_graph = flow.compile()
        # Graph visualization disabled to avoid Mermaid.INK API errors
        # try:
        #     # TODO: Change this path
        #     app_name = config("APP_NAME", default="ai_assistant")
        #     compiled_graph.get_graph().draw_mermaid_png(
        #         output_file_path=f"{curr_dir}/{app_name}/llm_agent/agents/{cls.agent_name}.png"
        #     )
        # except Exception as e:
        #     print("Unable to create or write created graph image file error: {}".format(e))

        return compiled_graph
