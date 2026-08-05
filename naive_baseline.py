from dotenv import load_dotenv
from groq import Groq
import os
import json
from tickets import tickets

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

results = []

for i, ticket in enumerate(tickets):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a customer support agent. Answer the customer's question."},
            {"role": "user", "content": ticket}
        ]
    )
    answer = response.choices[0].message.content
    results.append({"ticket": ticket, "naive_answer": answer})
    print(f"--- Ticket {i+1} ---")
    print(f"Q: {ticket}")
    print(f"A: {answer}\n")

with open("naive_baseline_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved all results to naive_baseline_results.json")