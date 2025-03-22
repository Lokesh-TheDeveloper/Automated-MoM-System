import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Jira API authentication
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {"Accept": "application/json"}

# Replace 'user@example.com' with the assignee's email
EMAIL = "shivakant1@lumiq.ai"

# API endpoint to fetch user details
url = f"{JIRA_URL}/rest/api/3/user/search?query={EMAIL}"

response = requests.get(url, auth=AUTH, headers=HEADERS)

if response.status_code == 200:
    users = response.json()
    for user in users:
        print(f"Display Name: {user['displayName']}, Account ID: {user['accountId']}")
else:
    print(f"❌ Error fetching user details: {response.json()}")
