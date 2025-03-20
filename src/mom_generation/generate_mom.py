import os
import jinja2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load the meeting summary
def load_summary(file_path="meeting_summary.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Jinja2 template for MoM
template_str = """
Meeting Minutes (MoM)
======================

**Meeting Summary:**
{{ summary }}

**Key Decisions:**
{% for decision in decisions %}
- {{ decision }}
{% endfor %}

**Action Items:**
{% for action in action_items %}
- {{ action.task }} → Assigned to {{ action.assignee }} (Due: {{ action.due_date }})
{% endfor %}

"""

def generate_mom(summary_text):
    """Generate a structured MoM document using Jinja2."""
    template = jinja2.Template(template_str)
    
    # Extract structured data from summary (assume format is correct)
    sections = summary_text.split("**")
    decisions = []
    action_items = []
    summary = sections[1].replace("Meeting Summary:", "").strip() if len(sections) > 1 else ""
    
    for section in sections:
        if "Key Decisions:" in section:
            decisions = [line.strip('- ') for line in section.split('\n') if line.startswith('-')]
        elif "Action Items:" in section:
            for line in section.split('\n'):
                if '→' in line:
                    parts = line.split('→')
                    task = parts[0].strip('- ').strip()
                    assigned_info = parts[1].split('(Due:')
                    assignee = assigned_info[0].strip()
                    due_date = assigned_info[1].replace(")", "").strip() if len(assigned_info) > 1 else ""
                    action_items.append({"task": task, "assignee": assignee, "due_date": due_date})
    
    # Render template
    mom_content = template.render(summary=summary, decisions=decisions, action_items=action_items)
    
    # Save MoM document
    with open("meeting_mom.txt", "w", encoding="utf-8") as f:
        f.write(mom_content)
    
    print("MoM document saved as meeting_mom.txt")

if __name__ == "__main__":
    print("Loading meeting summary...")
    summary_text = load_summary()
    print("Generating MoM document...")
    generate_mom(summary_text)
