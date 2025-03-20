import openai
import os
import textwrap
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load the transcript file
def load_transcript(file_path="transcript.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Chunk long transcripts into smaller parts
def chunk_text(text, chunk_size=4000):
    return textwrap.wrap(text, width=chunk_size)

# Generate summary using ChatGPT-4
def generate_summary(transcript_text):
    openai.api_key = OPENAI_API_KEY

    # Structure the prompt for better output
    prompt = f"""
    Summarize the following meeting transcript and extract key action items.
    Provide output in the following format:
    
    **Meeting Summary:** 
    [Brief Summary]
    
    **Key Decisions:**
    - Decision 1
    - Decision 2
    
    **Action Items:**
    - [Task] → Assigned to [Person] (Due: [Date])
    
    Transcript:
    {transcript_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes meeting transcripts and extracts key action items."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error generating summary:", e)
        return None

if __name__ == "__main__":
    print("Loading transcript...")
    transcript = load_transcript()

    print("Splitting transcript if needed...")
    transcript_chunks = chunk_text(transcript)

    full_summary = ""

    print("Generating summary and action items...")
    for chunk in transcript_chunks:
        summary = generate_summary(chunk)
        if summary:
            full_summary += summary + "\n\n"

    # Save the structured summary
    with open("meeting_summary.txt", "w", encoding="utf-8") as f:
        f.write(full_summary)

    print("Summary saved to meeting_summary.txt")