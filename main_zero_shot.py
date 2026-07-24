import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

# Read tickets
df = pd.read_csv("support_tickets_raw.csv")

results = []

print(f"Found {len(df)} tickets\n")

for index, row in df.iterrows():

    ticket_id = row["ticket_id"]
    ticket_text = row["ticket_text"]

    prompt = f"""
You are an AI support ticket classifier.

Classify the following support ticket.

Ticket:
{ticket_text}

Return ONLY valid JSON.

{{
    "category":"Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
    "urgency":"Low | Medium | High | Critical",
    "sentiment":"Positive | Neutral | Negative"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        output = response.choices[0].message.content.strip()

        output = output.replace("```json", "")
        output = output.replace("```", "")
        output = output.strip()

        prediction = json.loads(output)

        prediction["ticket_id"] = ticket_id

        results.append(prediction)

        print(f"✓ {index + 1}/{len(df)} {ticket_id}")

        time.sleep(1)

    except Exception as e:
        print(f"✗ {ticket_id}: {e}")

# Save CSV
result_df = pd.DataFrame(results)

result_df.to_csv("ticket_classifications.csv", index=False)

# Save JSON
result_df.to_json(
    "ticket_classifications.json",
    orient="records",
    indent=4
)

print("\n===================================")
print("Classification Completed!")
print("Files created:")
print("- ticket_classifications.csv")
print("- ticket_classifications.json")
print("===================================")