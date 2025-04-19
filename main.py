from gmail_fetcher import fetch_promotional_emails
from analyzer import analyze_email, analyze_email_for_expiry


# if __name__ == '__main__':
#     emails = fetch_promotional_emails(max_results=5)
#     for e in emails:
#         print(f"📨 Subject: {e['subject']} | From: {e['from']}")
#         analysis = analyze_email_for_expiry(e['body'])
#         print(analysis)
#         print('-' * 80)


def main():
    emails = fetch_promotional_emails(max_results=2)

    for idx, email in enumerate(emails):
        # print(f"\n📨 [{idx+1}] Subject: {email['subject']}")
        # print(f"From: {email['from']}")
        # print("\n🔍 Analyzing...")
        result = analyze_email(email['body'], model="phi")  # or "mistral", "llama3"
        print(idx, ". ", result)
        # print("-" * 60)


if __name__ == "__main__":
    main()
