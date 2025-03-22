import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL")  # Example: https://yourcompany.atlassian.net
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# Setup logging
logging.basicConfig(filename="task_status.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Jira API authentication
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {"Accept": "application/json"}

# Function to check task statuses
def get_jira_tasks():
    url = f"{JIRA_URL}/rest/api/3/search"
    query = {
        "jql": f"project={JIRA_PROJECT_KEY} AND status != 'Done'",
        "fields": ["summary", "assignee", "duedate", "status"]
    }
    
    response = requests.get(url, headers=HEADERS, auth=AUTH, params=query)
    
    if response.status_code == 200:
        tasks = response.json().get("issues", [])
        return tasks
    else:
        logging.error("Error fetching Jira tasks: %s", response.json())
        return []

if __name__ == "__main__":
    print("Checking Jira tasks...")
    tasks = get_jira_tasks()
    
    for task in tasks:
        task_key = task.get("key")
        summary = task["fields"].get("summary", "No summary")
        status = task["fields"].get("status", {}).get("name", "Unknown")
        due_date = task["fields"].get("duedate", "No due date")
        assignee = task["fields"].get("assignee", {}).get("displayName", "Unassigned")
        
        print(f"Task: {task_key} | {summary} | Status: {status} | Due: {due_date} | Assignee: {assignee}")
        logging.info(f"Checked task: {task_key} | Status: {status} | Due: {due_date}")
