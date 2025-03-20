import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL")  # Example: https://yourcompany.atlassian.net
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Jira API authentication
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {"Content-Type": "application/json"}

# Create a Jira task
def create_jira_task(summary, description, assignee=None, due_date=None):
    data = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }
    }
    
    # Add assignee if provided
    if assignee:
        data["fields"]["assignee"] = {"accountId": assignee}
    
    # Add due date if provided
    if due_date:
        data["fields"]["duedate"] = due_date
    
    response = requests.post(f"{JIRA_URL}/rest/api/3/issue", auth=AUTH, headers=HEADERS, data=json.dumps(data))
    
    if response.status_code == 201:
        print(f"Jira Task Created: {response.json().get('key')}")
    else:
        print("Error creating Jira task:", response.json())

if __name__ == "__main__":
    # Example usage (Replace with extracted action items from MoM summary)
    create_jira_task(
        summary="Follow up on budget approval",
        description="Ensure the finance team reviews the budget proposal.",
        assignee=None,  # Replace with a valid Jira user account ID
        due_date="2025-03-30"
    )
