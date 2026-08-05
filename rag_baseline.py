from dotenv import load_dotenv
from groq import Groq
import chromadb
import os
import json
from tickets import tickets
from policies import policies

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- Step 1: Set up Chroma and load our policy docs into it ---
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="support_policies")

collection.add(
    documents=list(policies.values()),
    ids=list(policies.keys())
)

# --- Step 2: For each ticket, retrieve relevant policy, then answer using it ---
results = []

for i, ticket in enumerate(tickets):
    # Retrieve the 2 most relevant policy docs for this ticket
    retrieved = collection.query(
        query_texts=[ticket],
        n_results=2
    )
    retrieved_docs = retrieved["documents"][0]
    retrieved_context = "\n\n".join(retrieved_docs)

    # Now answer USING the retrieved context, not from memory
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"You are a customer support agent. Answer the customer's question using ONLY the policy information below. If the policy doesn't cover something (like a specific order's real-time status), say so honestly instead of guessing.\n\nRELEVANT POLICIES:\n{retrieved_context}"
            },
            {"role": "user", "content": ticket}
        ]
    )
    answer = response.choices[0].message.content

    results.append({
        "ticket": ticket,
        "retrieved_context": retrieved_context,
        "rag_answer": answer
    })

    print(f"--- Ticket {i+1} ---")
    print(f"Q: {ticket}")
    print(f"A: {answer}\n")

with open("rag_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved all results to rag_results.json")