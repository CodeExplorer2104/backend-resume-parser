import json
from gemini_utils import extract_resume_data

def parse_resume(text):
    try:
        result = extract_resume_data(text)
        clean = result.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        return fallback_parser(text)

def fallback_parser(text):
    SKILLS_DB = ["Python", "Java", "SQL", "Machine Learning", "Deep Learning", 
                 "OpenCV", "YOLO", "TensorFlow", "NumPy", "React", "JavaScript",
                 "FastAPI", "FAISS", "Docker", "AWS", "Flask"]
    skills = [s for s in SKILLS_DB if s.lower() in text.lower()]
    return {
        "skills": list(set(skills)),
        "projects": [],
        "experience": [],
        "education": []
    }