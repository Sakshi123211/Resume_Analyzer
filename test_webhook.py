import requests
import os
from dotenv import load_dotenv

load_dotenv()

webhook_url = os.getenv('N8N_WEBHOOK_URL')

print(f"Testing webhook: {webhook_url}")

test_data = {
    "name": "Test Candidate",
    "email": "test@example.com",
    "score": 85,
    "experience": "5 years",
    "skills": "Python, AI, ML",
    "summary": "This is a test candidate"
}

try:
    response = requests.post(webhook_url, json=test_data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print("✅ Webhook is working!" if response.status_code == 200 else "❌ Webhook failed")
except Exception as e:
    print(f"❌ Error: {str(e)}")
