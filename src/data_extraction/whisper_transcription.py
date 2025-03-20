import whisper
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define path to meeting recording
MEETING_RECORDING_PATH = os.getenv("MEETING_RECORDING_PATH", "meeting_recording.mp4")

def transcribe_audio(file_path):
    """Transcribe audio using Whisper AI."""
    print("Loading Whisper model...")
    model = whisper.load_model("base")  # Load the Whisper AI model
    print("Transcribing audio...")
    result = model.transcribe(file_path)
    
    transcript_text = result["text"]
    print("Transcription Complete.")
    return transcript_text

if __name__ == "__main__":
    if os.path.exists(MEETING_RECORDING_PATH):
        transcript = transcribe_audio(MEETING_RECORDING_PATH)
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        print("Transcript saved to transcript.txt")
    else:
        print(f"Error: Meeting recording file '{MEETING_RECORDING_PATH}' not found.")
