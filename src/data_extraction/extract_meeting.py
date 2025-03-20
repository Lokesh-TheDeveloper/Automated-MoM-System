import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
ACCESS_TOKEN = os.getenv("MS_GRAPH_ACCESS_TOKEN")
MEETING_ID = os.getenv("MEETING_ID")
BASE_URL = "https://graph.microsoft.com/v1.0/me/onlineMeetings/"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_meeting_details():
    url = f"{BASE_URL}{MEETING_ID}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching meeting details:", response.json())
        return None

def get_meeting_transcript():
    url = f"{BASE_URL}{MEETING_ID}/transcripts"
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            transcript_data = response.json()
            transcript_text = transcript_data.get("content", "")  # Extract text
            
            # Save transcript to a file
            with open("meeting_transcript.txt", "w", encoding="utf-8") as f:
                f.write(transcript_text)
            
            print("Transcript saved to meeting_transcript.txt")
            return transcript_text
        else:
            print("Transcript not ready. Checking again in 5 minutes...")
            time.sleep(300)  # Wait 5 minutes before retrying


def get_meeting_chat():
    meeting_data = get_meeting_details()
    if meeting_data and "chatInfo" in meeting_data:
        chat_id = meeting_data["chatInfo"]["threadId"]
        chat_url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
        response = requests.get(chat_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching chat messages:", response.json())
            return None

if __name__ == "__main__":
    print("Fetching meeting transcript...")
    transcript = get_meeting_transcript()
    if transcript is None:
        print("Transcript not available. Consider using Whisper AI for transcription.")
    print("Fetching meeting chat messages...")
    chat_messages = get_meeting_chat()
    print("Meeting Data Extraction Completed.")
