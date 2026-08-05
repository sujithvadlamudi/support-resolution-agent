import json
from graph import graph
from tickets import tickets

results = []

for i, ticket in enumerate(tickets):
    print(f"\n=== Ticket {i+1} ===")
    print(f"Q: {ticket}")

    final_state = graph.invoke({"ticket": ticket})
    answer = final_state["final_answer"]

    print(f"A: {answer}")

    results.append({
        "ticket": ticket,
        "needs_order_check": final_state.get("needs_order_check"),
        "order_id": final_state.get("order_id"),
        "order_info": final_state.get("order_info"),
        "final_answer": answer
    })

with open("agent_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved all results to agent_results.json")