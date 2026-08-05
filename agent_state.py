from typing import TypedDict, Optional

class TicketState(TypedDict):
    ticket: str                      # the customer's question
    needs_order_check: bool          # decision made by the classify step
    order_id: Optional[str]          # extracted from the ticket, if any
    order_info: Optional[dict]       # result from the tool, if we called it
    retrieved_policy: str            # policy text pulled from our knowledge base
    final_answer: str                # the answer we give the customer