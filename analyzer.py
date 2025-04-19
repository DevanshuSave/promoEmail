# analyzer.py

import openai
import subprocess

client = openai.OpenAI(api_key="<API_KEY>")


def analyze_email_for_expiry(email_text):
    """Send the email text to GPT and return a summary with expiry info."""
    system_msg = (
        "You are an assistant that extracts promotional offers and expiration details from emails. "
        "If no expiry is mentioned, say 'No expiry date found'."
    )

    user_msg = f"""Email content:
{email_text}

Your job:
- Only Yes/No reply whether this is a promotional offer? (yes/no)
- What is the promotion?
- When does it expire? (If no date, skip email)
"""
    openai_client = openai.OpenAI()
    response = openai_client.chat.completions.create(
        model="gpt-4.1",  # or "gpt-4"
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2
    )

    return response['choices'][0]['message']['content']


def analyze_email(email_text, model="phi"):
    prompt = f"""
Extract the promotional offer and expiration date from the following email.

\"\"\"
{email_text}
\"\"\"

Reply with a json format answering these 3 questions:
- Only Yes/No reply whether this is a promotional offer? (yes/no)
- What is the promotion?
- When does it expire? If no expiry, say "No expiry date found".
"""

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return result.stdout.decode('utf-8')
