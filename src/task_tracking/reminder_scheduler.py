import requests
import os
import smtplib
import logging
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Setup logging
logging.basicConfig(filename="reminder.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Jira API authentication
AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {"Accept": "application/json"}

# Function to fetch overdue Jira tasks
def get_overdue_tasks():
    url = f"{JIRA_URL}/rest/api/3/search"
    query = {
        "jql": f"project={JIRA_PROJECT_KEY} AND status != 'Done' AND duedate <= now()",
        "fields": ["summary", "assignee", "duedate"]
    }
    
    response = requests.get(url, headers=HEADERS, auth=AUTH, params=query)
    
    if response.status_code == 200:
        return response.json().get("issues", [])
    else:
        logging.error("Error fetching overdue Jira tasks: %s", response.json())
        return []

# Function to send email reminders
def send_reminder(to_email, task_summary, due_date):
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Task Reminder - Overdue Task"

    body = f"""
    Hello,
    
    This is a reminder that the following task is overdue:
    
    Task: {task_summary}
    Due Date: {due_date}
    
    Please complete it as soon as possible.
    
    Best,
    Automated MoM System
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        logging.info(f"Reminder sent to {to_email} for task: {task_summary}")
    except Exception as e:
        logging.error(f"Error sending reminder to {to_email}: {e}")

if __name__ == "__main__":
    print("Checking for overdue tasks...")
    overdue_tasks = get_overdue_tasks()
    
    for task in overdue_tasks:
        task_summary = task["fields"].get("summary", "No summary")
        due_date = task["fields"].get("duedate", "No due date")
        assignee = task["fields"].get("assignee", {}).get("emailAddress", "")
        
        if assignee:
            print(f"Sending reminder for task: {task_summary} to {assignee}")
            send_reminder(assignee, task_summary, due_date)
        else:
            logging.warning(f"No assignee email found for task: {task_summary}")
