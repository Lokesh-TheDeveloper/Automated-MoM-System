import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("MS_GRAPH_ACCESS_TOKEN")
ONEDRIVE_FOLDER = os.getenv("ONEDRIVE_FOLDER", "MoM_Folder")
FILE_PATH = "meeting_mom.txt"

# Upload URL (OneDrive API)
UPLOAD_URL = f"https://graph.microsoft.com/v1.0/me/drive/root:/{ONEDRIVE_FOLDER}/meeting_mom.txt:/content"

# Upload function
def upload_to_onedrive():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found!")
        return None
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    with open(FILE_PATH, "rb") as file:
        response = requests.put(UPLOAD_URL, headers=headers, data=file)
    
    if response.status_code == 201:
        print("MoM successfully uploaded to OneDrive.")
        return response.json().get("id")  # Return file ID
    else:
        print("Error uploading file:", response.json())
        return None

# Generate shareable link
def generate_share_link(file_id):
    SHARE_URL = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/createLink"
    payload = {"type": "view", "scope": "organization"}
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    
    response = requests.post(SHARE_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        share_link = response.json().get("link", {}).get("webUrl")
        print(f"Shareable MoM Link: {share_link}")
        return share_link
    else:
        print("Error generating share link:", response.json())
        return None

if __name__ == "__main__":
    print("Uploading MoM to OneDrive...")
    file_id = upload_to_onedrive()
    if file_id:
        generate_share_link(file_id)
