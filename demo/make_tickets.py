#!/usr/bin/env python3
"""Generate a synthetic customer-service ticket CSV for laya-train dry-run demo."""
import csv
import random

random.seed(42)

BILLING = [
    "We were billed twice for March.",
    "My invoice shows a charge I never approved.",
    "Please refund the duplicate payment on invoice #{}.",
    "The annual plan was charged but I downgraded to monthly last week.",
    "Card was charged {} dollars instead of the advertised price.",
]
TECHNICAL = [
    "The app crashes on startup since the last update.",
    "Login page returns a 500 error in Chrome.",
    "Export to CSV has been failing for three days.",
    "Webhook deliveries stopped after we rotated the API key.",
    "Search results take over 30 seconds to load.",
]
ACCOUNT = [
    "I need to change the email on my account.",
    "Please close my account and delete my data.",
    "How do I add a teammate to the workspace?",
    "Two-factor authentication lockout, recovery codes lost.",
    "Transfer ownership of the org to another admin.",
]
SECURITY = [
    "I received a phishing email pretending to be your billing team.",
    "Someone logged into my account from another country.",
    "Suspicious API key was created on our org overnight.",
    "Please report abuse: a user is leaking credentials in forum posts.",
    "Our security scan flagged an exposed token in a public repo.",
]
SPAM = [
    "BUY NOW cheap followers!!! visit spam-site.example",
    "Congratulations you won a prize, click here to claim.",
]

rows = []
for i in range(300):
    for dept, templates in (("billing", BILLING), ("technical", TECHNICAL),
                            ("account", ACCOUNT), ("security", SECURITY)):
        t = random.choice(templates)
        body = t.format(random.randint(1000, 9999)) if "{}" in t else t
        rows.append({"ticket_id": 1000 + len(rows), "body": body, "department": dept})

# Deliberately bad rows: empty label, empty text, unknown label
rows.append({"ticket_id": 99990, "body": "This ticket has no department.", "department": ""})
rows.append({"ticket_id": 99991, "body": "", "department": "billing"})
rows.append({"ticket_id": 99992, "body": "", "department": ""})

random.shuffle(rows)

with open("/Users/johnson/WorkBuddy/laya-finetune/demo/tickets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["ticket_id", "body", "department"])
    writer.writeheader()
    writer.writerows(rows)

print(f"written {len(rows)} rows to tickets.csv")
