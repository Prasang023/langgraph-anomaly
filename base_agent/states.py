import operator
from typing import Any, List, TypeVar, TypedDict, Union, Annotated
from uuid import UUID
from langchain.schema import BaseMessage


def annonated_replace_aggregator(old_value, new_value):
    if new_value is not None:
        return new_value
    return old_value


class BaseNodeState(TypedDict):
    response_id: Annotated[UUID, annonated_replace_aggregator]
    agent_name: Annotated[str, annonated_replace_aggregator]
    chat_history: Annotated[List[BaseMessage], annonated_replace_aggregator]
    data_required: Annotated[List[str], annonated_replace_aggregator]
    user_data: Annotated[dict[str, dict], annonated_replace_aggregator]
    user_data_meta: Annotated[dict, annonated_replace_aggregator]
    request_tokens_used: Annotated[int, operator.add]
    response_tokens_used: Annotated[int, operator.add]
    chat_type: Annotated[str, annonated_replace_aggregator]
    session_store: Annotated[dict[str, Any], annonated_replace_aggregator]


BaseNodeStateTypeVar = TypeVar("BaseNodeStateTypeVar", bound=BaseNodeState)