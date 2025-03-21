import smtplib
import os
import requests
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ACCESS_TOKEN = os.getenv("MS_GRAPH_ACCESS_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")

# Fetch meeting participants from Microsoft Graph API
def get_meeting_participants():
    url = f"https://graph.microsoft.com/v1.0/me/onlineMeetings/{MEETING_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        meeting_data = response.json()
        participants = [
            attendee["emailAddress"]["address"]
            for attendee in meeting_data.get("participants", {}).get("attendees", [])
        ]
        return participants
    else:
        print("Error fetching participants:", response.json())
        return []

# Email function
def send_mom_email(to_emails, mom_link):
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = "Minutes of Meeting (MoM) - Automated System"

    # Email body
    body = f"""
    Hello Team,
    
    The MoM document for our recent meeting is available here:
    {mom_link}
    
    Please review and update action items as needed.
    
    Best,
    Automated MoM System
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_emails, msg.as_string())
        server.quit()
        print("MoM email successfully sent.")
    except Exception as e:
        print("Error sending email:", e)

if __name__ == "__main__":
    print("Fetching meeting participants...")
    recipient_emails = get_meeting_participants()
    
    if recipient_emails:
        mom_link = "https://onedrive.com/shared-link-to-mom"  # Replace with actual OneDrive link
        print("Sending MoM email...")
        send_mom_email(recipient_emails, mom_link)
    else:
        print("No participants found. Email not sent.")
