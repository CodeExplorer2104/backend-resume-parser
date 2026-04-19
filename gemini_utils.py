from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)
def extract_resume_data(text):
    prompt = f"""
Extract structured data from this resume.
Return ONLY valid JSON, no markdown, no explanation.

Resume:
{text}

Return exactly this format:
{{
  "name": "",
  "skills": [],
  "projects": [],
  "experience": [],
  "education": []
}}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_recommendations(profile):
    prompt = f"""
Based on this candidate profile:
{profile}

Provide:
1. Skill Gaps: skills they are missing for top tech roles
2. Suggested Courses: specific courses to fill gaps
3. Career Advice: next steps for career growth

Be specific and concise.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content