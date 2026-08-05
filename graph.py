from langgraph.graph import StateGraph, END
from agent_state import TicketState
from nodes import classify, check_order, retrieve_policy, generate_answer


def route_after_classify(state: dict) -> str:
    """Decide which node runs next, based on the classify decision."""
    if state["needs_order_check"]:
        return "check_order"
    else:
        return "retrieve_policy"


# Build the graph
builder = StateGraph(TicketState)

builder.add_node("classify", classify)
builder.add_node("check_order", check_order)
builder.add_node("retrieve_policy", retrieve_policy)
builder.add_node("generate_answer", generate_answer)

builder.set_entry_point("classify")

builder.add_conditional_edges(
    "classify",
    route_after_classify,
    {
        "check_order": "check_order",
        "retrieve_policy": "retrieve_policy"
    }
)

builder.add_edge("check_order", "retrieve_policy")
builder.add_edge("retrieve_policy", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()