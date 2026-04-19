# Resume Matching Multi-Agent System

An AI-powered resume matching system built with AutoGen Studio and FastAPI. It uses a multi-agent pipeline to parse resumes, match them to jobs, identify skill gaps, and provide career recommendations.

---

## System Requirements

- Python 3.11
- pip
- AutoGen Studio
- FastAPI

---

## Project Structure

```
resume-agent-system/
├── backend/
│   ├── main.py
│   ├── gemini_utils.py
│   └── requirements.txt
└── README.md
```

---

## Setup and Installation

### Step 1 - Clone or Download the Project

Download and extract the project to your local machine. Open a terminal and navigate to the project folder:

```
cd D:\Downloads\resume-agent-system
```

### Step 2 - Install Backend Dependencies

```
cd backend
pip install -r requirements.txt
```

If you do not have a requirements.txt, install manually:

```
pip install fastapi uvicorn openai requests sentence-transformers scikit-learn
```

### Step 3 - Install AutoGen Studio

```
pip install autogenstudio
```

### Step 4 - Configure API Key

Open `backend/gemini_utils.py` and configure:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-openrouter-api-key-here",
    base_url="https://openrouter.ai/api/v1"
)
```

Get your API key from: https://openrouter.ai/keys

---

## Running the System

You need to run two things at the same time. Open two terminals.

### Terminal 1 - Start Backend

```
cd D:\Downloads\resume-agent-system\backend
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2 - Start AutoGen Studio

```
autogenstudio ui --port 8080
```

Open:
```
http://127.0.0.1:8080
```

---

## Importing the Agent Team

1. Open AutoGen Studio
2. Go to **Team Builder**
3. Click **New Team**
4. Open **JSON tab**
5. Paste team JSON config
6. Click **Save**
7. Click **Test Team**

---

## How to Use

### Run 1
```
hi
```

### Run 2
```
A   (Applicant)
B   (Recruiter)
```

### Run 3
Paste resume or job requirements

---

## Sample Resume

```
John Smith

SUMMARY
Software Engineer with 3 years of experience in Python and web development.

SKILLS
Python, Django, REST APIs, JavaScript, React, SQL, PostgreSQL, Docker, Git, Linux

EXPERIENCE
Software Engineer - TechCorp Solutions (2021 - 2024)
- Built REST APIs using Django and Python serving 50k daily users
- Migrated legacy SQL database to PostgreSQL improving query speed by 40%
- Containerized applications using Docker reducing deployment time by 30%

EDUCATION
Bachelor of Engineering in Computer Science
Pune University - 2020
```

---

## Sample Recruiter Query

```
Looking for Senior Python Developer with Django, REST APIs, Docker, 3+ years experience. Bonus: React/PostgreSQL.
```

---

## Agents

| Agent | Role |
|------|------|
| intake_agent | User interaction |
| resume_parser | Extracts data |
| structurer | Formats data |
| matcher | Matches roles |
| recommender | Suggests improvements |
| trend_analyzer | Market insights |

---

## Flow

### Applicant
```
Resume → intake → parser → structurer → matcher → recommender → trends
```

### Recruiter
```
Requirements → intake → parser → structurer → matcher → recommender → trends
```

---

## Common Issues

### 401 Error
Check API key and base_url

### Agents say SKIP
Ensure resume has:
```
SKILLS
EXPERIENCE
EDUCATION
```

### intake_agent repeats
Use separate runs for `hi` and `A/B`

### Port Issue
```
netstat -ano | findstr :8000
```

---

## API

```
POST http://127.0.0.1:8000/match
```

### Request
```json
{
  "resume": "text"
}
```

### Response
```json
{
  "parsed_data": {},
  "matched_jobs": [],
  "recommendations": ""
}
```

---

## Tech Stack

- AutoGen Studio
- FastAPI
- OpenRouter
- GPT-4o-mini
- Python 3.11
- Uvicorn