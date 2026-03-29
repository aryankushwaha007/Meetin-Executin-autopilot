import json
import os
import re
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Define the Pydantic schema for the Gemini Structured Output
class ExtractedTask(BaseModel):
    title: str = Field(description="A concise, actionable title for the task")
    description: str = Field(description="A brief description of what needs to be done")
    owner: Optional[str] = Field(None, description="The name of the person assigned to the task, if mentioned. Extremely important: leave as null if not explicitly assigned.")
    priority: str = Field(description="The priority of the task: 'low', 'medium', or 'high'")
    risk_level: str = Field(description="The risk level of the task: 'low', 'medium', or 'high'")
    dependencies: Optional[str] = Field(None, description="Any tasks that must be completed before this one")
    confidence: float = Field(description="A float between 0.0 and 1.0 representing confidence in this extraction")

class TaskList(BaseModel):
    tasks: List[ExtractedTask]

# Initialize the Gemini client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def extract_tasks_from_transcript(transcript: str) -> List[dict]:
    """
    Extracts action items from a transcript using Gemini 2.5 Flash if available,
    falling back to the deterministic mock logic if no API key is set.
    """
    if client:
        try:
            prompt = f"""You are an autonomous enterprise Orchestrator Agent named AutopilotOS. 
            Critically analyze the following meeting transcript.
            Extract all distinct action items, decisions, and tasks. 
            Be brutal about finding dependencies and assessing risk. If a task involves security, compliance, or money, its risk_level is 'high'. 
            If no owner is clearly assigned to a task, absolutely ensure the 'owner' field is null so the Owner Assignment Agent can take over.
            
            Transcript:
            \"\"\"{transcript}\"\"\"
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': TaskList,
                },
            )
            
            # The response is directly unmarshalled against the Pydantic schema
            if response.parsed:
                extracted_list: TaskList = response.parsed
                # Convert Pydantic objects back to the dict format expected by the DB logic
                return [task.model_dump() for task in extracted_list.tasks]
            
        except Exception as e:
            print(f"[Extractor] LLM Error: {e}. Falling back to mock data.")

    # --- FALLBACK MOCK LOGIC ---
    print("[Extractor] No valid GEMINI_API_KEY found or API failed. Using mock extraction fallback.")
    tasks = []
    
    if "database migration" in transcript.lower():
        tasks.append({
            "title": "Perform database migration for new schema",
            "description": "The new user profile schema requires a database migration script.",
            "owner": "Sarah",
            "priority": "high",
            "risk_level": "medium",
            "dependencies": None,
            "confidence": 0.95
        })
    
    if "update the marketing landing page" in transcript.lower():
        tasks.append({
            "title": "Update marketing landing page",
            "description": "Add the new enterprise features to the homepage.",
            "owner": "Mike",
            "priority": "medium",
            "risk_level": "low",
            "dependencies": None,
            "confidence": 0.88
        })
        
    if "security audit" in transcript.lower() or "compliance" in transcript.lower():
        tasks.append({
            "title": "Conduct Q3 Security Audit",
            "description": "Review IAM roles and compliance checklist.",
            "owner": None,
            "priority": "high",
            "risk_level": "high",
            "dependencies": None,
            "confidence": 0.75
        })

    if not tasks:
        tasks.append({
                "title": "Review meeting action items",
                "description": "Follow up on generic action items discussed.",
                "owner": "Team Lead",
                "priority": "medium",
                "risk_level": "low",
                "dependencies": None,
                "confidence": 0.60
            })
            
    return tasks
