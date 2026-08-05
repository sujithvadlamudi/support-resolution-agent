from dotenv import load_dotenv
from groq import Groq
import os
import re
import chromadb
from tools import get_order_status
from policies import policies

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Set up the vector store once, when this file is first loaded
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="support_policies")
collection.add(documents=list(policies.values()), ids=list(policies.keys()))


def classify(state: dict) -> dict:
    """Decide if this ticket needs a real order lookup, and extract the order ID if present."""
    ticket = state["ticket"]

    order_id_match = re.search(r"#?(\d{4})", ticket)
    order_id = order_id_match.group(1) if order_id_match else None

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You classify support tickets. Reply with ONLY 'yes' or 'no': does answering this ticket require checking a specific order's real-time status (not just general policy)?"
            },
            {"role": "user", "content": ticket}
        ]
    )
    decision = response.choices[0].message.content.strip().lower()
    needs_order_check = "yes" in decision and order_id is not None

    print(f"[classify] needs_order_check={needs_order_check}, order_id={order_id}")

    return {
        "needs_order_check": needs_order_check,
        "order_id": order_id
    }


def check_order(state: dict) -> dict:
    """Call the mock tool to get real order data."""
    order_id = state["order_id"]
    order_info = get_order_status(order_id)
    print(f"[check_order] order_info={order_info}")
    return {"order_info": order_info}


def retrieve_policy(state: dict) -> dict:
    """Retrieve the most relevant policy docs for this ticket."""
    ticket = state["ticket"]
    results = collection.query(query_texts=[ticket], n_results=2)
    retrieved_context = "\n\n".join(results["documents"][0])
    print(f"[retrieve_policy] retrieved {len(results['documents'][0])} docs")
    return {"retrieved_policy": retrieved_context}


def generate_answer(state: dict) -> dict:
    """Combine policy + order info (if any) into a final answer."""
    ticket = state["ticket"]
    retrieved_policy = state["retrieved_policy"]
    order_info = state.get("order_info")

    context = f"RELEVANT POLICIES:\n{retrieved_policy}"
    if order_info:
        context += f"\n\nREAL ORDER DATA:\n{order_info}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"You are a customer support agent. Answer using ONLY the information below. If order data is provided, use it directly (e.g., to determine refund eligibility based on real days-since-ordered). Be specific and helpful, not vague.\n\n{context}"
            },
            {"role": "user", "content": ticket}
        ]
    )
    answer = response.choices[0].message.content
    print(f"[generate_answer] answer generated")

    return {"final_answer": answer}