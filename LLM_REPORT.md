# LLM Powered Ticket Classification Report

## Model Used

- Provider: Groq
- Model: llama-3.3-70b-versatile

---

## Prompt Strategy 1 - Zero-shot

```
You are an AI support ticket classifier.

Classify the following support ticket.

Ticket:
{ticket_text}

Return ONLY valid JSON.

{
    "category":"Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
    "urgency":"Low | Medium | High | Critical",
    "sentiment":"Positive | Neutral | Negative"
}
```

---

## Prompt Strategy 2 - Few-shot

```
You are an AI support ticket classifier.

Example 1

Ticket:
I was charged twice for my monthly subscription.

Output:
{
    "category":"Billing",
    "urgency":"High",
    "sentiment":"Negative"
}

Example 2

Ticket:
I forgot my password and cannot log into my account.

Output:
{
    "category":"Account Access",
    "urgency":"Medium",
    "sentiment":"Neutral"
}

Example 3

Ticket:
The mobile app crashes whenever I try to upload a file.

Output:
{
    "category":"Technical Issue",
    "urgency":"High",
    "sentiment":"Negative"
}

Now classify this ticket and return ONLY valid JSON.
```

---

## Accuracy Comparison (14 Validation Tickets)

| Field | Zero-shot | Few-shot |
|--------|-----------|-----------|
| Category | 92.86% (13/14) | 85.71% (12/14) |
| Urgency | 64.29% (9/14) | 64.29% (9/14) |
| Sentiment | 92.86% (13/14) | 92.86% (13/14) |

---

## Winning Strategy

The Zero-shot prompt was selected because it achieved the highest category accuracy while matching the Few-shot prompt on urgency and sentiment.

---

## Validation Logic

The pipeline validates every response by:

- Checking that the response is valid JSON.
- Verifying that all required fields are present.
- Ensuring the values belong to the allowed categories.
- Skipping invalid responses and logging the error instead of stopping the pipeline.

---

## Observations

- Successfully classified all 45 support tickets.
- Produced structured JSON output for every ticket.
- Groq's Llama 3.3 70B model generated consistent results.
- No invalid JSON responses were encountered during the final run.

---

## Output Files

- ticket_classifications.csv
- ticket_classifications.json
- ticket_classifications_few_shot.csv
- ticket_classifications_few_shot.json