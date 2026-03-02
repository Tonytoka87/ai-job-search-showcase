"""
ai_writer_demo.py
Generic architectural example of the AI drafting approach.
This script demonstrates how PDF text and raw markdown job postings
are combined via Google's Gemini API to draft personalized applications.
"""

from google import genai
import os
from pypdf import PdfReader

# Generalized system prompt instructing the AI on how to behave
SYSTEM_PROMPT = """
You are an expert career advisor and ghostwriter. Your job is to generate a cover letter 
draft that feels authentic, methodical, and professionally grounded.

DECISION LOGIC:
- Analyze the provided job description.
- Align the candidate's skills from the provided CV with the core requirements of the role.

TONE & STYLE:
- Grounded, methodical, and professional. 
- Avoid classic "salesman" language and empty buzzwords.
- Honest matching: If a required skill (e.g., Python) isn't the candidate's core strength, angle it as "technically curious and fast learner".

Never hallucinate experiences not present in the CV.
"""

def extract_pdf_text(path: str) -> str:
    """Helper function to read the local CV."""
    try:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

class ApplicationGenerator:
    def __init__(self, gemini_api_key: str):
        self.api_key = gemini_api_key
        # Initialize client
        self.client = genai.Client(api_key=self.api_key)

    def generate_draft(self, job_title: str, job_description: str, cv_text: str) -> str:
        """
        Takes the extracted metadata from the scraper and the CV text,
        then queries the LLM for a tailored draft.
        """
        combined_prompt = f"""
        JOB TITLE: {job_title}
        
        JOB DESCRIPTION (Markdown):
        {job_description}
        
        CANDIDATE CV (Text):
        {cv_text}
        
        Write a cover letter according to the system prompt instructions.
        """

        try:
            # We use gemini-2.5-flash for speed and cost efficiency on drafts
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=combined_prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7, 
                ),
            )
            return response.text
        except Exception as e:
            return f"Generation failed: {e}"

if __name__ == "__main__":
    cv_text = extract_pdf_text("path/to/resume.pdf")
    generator = ApplicationGenerator("your-api-key")
    
    draft = generator.generate_draft(
        job_title="Senior IT Consultant",
        job_description="Seeking a candidate with strong architecture and integration skills...",
        cv_text=cv_text
    )
    
    print(draft)
