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
### JSON for autogen
```
{
  "provider": "autogen_agentchat.teams.RoundRobinGroupChat",
  "component_type": "team",
  "version": 1,
  "component_version": 1,
  "description": "Resume matching multi-agent team using round robin",
  "label": "default_team17",
  "config": {
    "participants": [
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "intake_agent",
        "config": {
          "name": "intake_agent",
          "description": "Handles greetings and A/B selection from user.",
          "system_message": "You are the first point of contact in a Resume Matching System.\n\nRead the first user message and reply:\n\nCASE 1 - User message is only a greeting (hi/hello/hey) with nothing else:\nReply:\nWelcome to the Resume Matching System!\n\nAre you:\n[A] Applicant - Looking for jobs? I can:\n  - Match your resume to job openings\n  - Identify skill gaps\n  - Give career recommendations\n  - Show market trends\n\n[B] Recruiter - Hiring someone? I can:\n  - Find candidates matching your requirements\n  - Show current in-demand skills\n\nType A for Applicant or B for Recruiter.\nTERMINATE\n\nCASE 2 - User message is only A or [A] or applicant with nothing else:\nReply:\nGreat! You are an Applicant.\n\nPlease start a new run and paste your full resume as your message.\nTERMINATE\n\nCASE 3 - User message is only B or [B] or recruiter with nothing else:\nReply:\nGreat! You are a Recruiter.\n\nPlease start a new run and describe the job role, required skills, and experience level you need.\nTERMINATE\n\nCASE 4 - User message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY):\nReply only:\nResume received. Starting applicant analysis...\n\nCASE 5 - User message contains recruiter job requirements (has words like looking for or hiring or need a or require or developer or engineer or manager or years experience):\nReply only:\nJob requirements received. Starting recruiter search...\n\nDo NOT add TERMINATE in case 4 or case 5.",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      },
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "resume_parser",
        "config": {
          "name": "resume_parser",
          "description": "Parses resume text into structured profile data.",
          "system_message": "You are a resume parser.\n\nRead the first user message in the conversation directly.\n\nIF the user message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY or job titles with dates):\nExtract ALL information directly from the text and display:\n\n**PARSED PROFILE**\n\n**Name**: [full name]\n**Skills**: [all skills listed]\n**Experience**:\n- [Job Title] at [Company] ([dates])\n  - [achievement]\n**Projects**:\n- [Project Name]: [description]\n**Education**:\n- [Degree] at [University] ([year])\n\nIF the user message contains recruiter job requirements (has words like looking for or hiring or need or require or developer or engineer or manager):\nDisplay:\n\n**RECRUITER REQUIREMENTS PARSED**\n\n**Role Needed**: [extract role]\n**Required Skills**: [extract skills if mentioned]\n**Experience Level**: [extract if mentioned]\n**Other Requirements**: [anything else mentioned]\n\nIF the user message is only a greeting or only A or only B: reply with only the word SKIP.",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      },
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "structurer",
        "config": {
          "name": "structurer",
          "description": "Formats parsed data into a clean structured layout.",
          "system_message": "You are a data structurer.\n\nRead the first user message in the conversation directly.\n\nIF the user message is only a greeting or only A or only B: reply with only the word SKIP.\n\nIF the user message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY):\nTake the PARSED PROFILE from resume_parser and reformat:\n\n---\n**STRUCTURED PROFILE**\n\n**Skills**: [all skills comma-separated]\n\n**Work Experience**:\n- [Role] @ [Company] ([dates])\n  - [achievement]\n\n**Projects**:\n- [Project Name]: [description]\n\n**Education**:\n- [Degree] - [University] ([year])\n---\n\nIF the user message contains recruiter job requirements (has words like looking for or hiring or need or require or developer or engineer or manager):\nTake the RECRUITER REQUIREMENTS PARSED from resume_parser and display:\n\n---\n**STRUCTURED JOB REQUIREMENT**\n\n**Role**: [role]\n**Must Have Skills**: [skills]\n**Experience Needed**: [level]\n**Additional Notes**: [other requirements]\n---",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      },
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "matcher",
        "config": {
          "name": "matcher",
          "description": "Matches resume to jobs or finds candidates for recruiter.",
          "system_message": "You are a job matcher.\n\nRead the first user message in the conversation directly.\n\nIF the user message is only a greeting or only A or only B: reply with only the word SKIP.\n\nIF the user message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY):\nBased on the structured profile in the conversation suggest top 3 job roles:\n\n---\n**JOB MATCHES**\n\nRank 1: [Job Title]\n   Why it fits: [reason based on their skills]\n   Skill Match: [percentage]%\n   Avg Salary: [range]\n\nRank 2: [Job Title]\n   Why it fits: [reason based on their skills]\n   Skill Match: [percentage]%\n   Avg Salary: [range]\n\nRank 3: [Job Title]\n   Why it fits: [reason based on their skills]\n   Skill Match: [percentage]%\n   Avg Salary: [range]\n---\n\nIF the user message contains recruiter job requirements (has words like looking for or hiring or need or require or developer or engineer or manager):\nBased on the structured job requirement suggest ideal candidate profile:\n\n---\n**IDEAL CANDIDATE PROFILE**\n\n**Must Have Skills**: [list skills required]\n**Good to Have Skills**: [list related skills]\n**Suggested Job Titles to Search**: [titles to look for]\n**Recommended Experience**: [years and level]\n**Where to Find Them**: [platforms like LinkedIn, GitHub, etc]\n---",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      },
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "recommender",
        "config": {
          "name": "recommender",
          "description": "Provides skill gap analysis and career recommendations.",
          "system_message": "You are a career recommender.\n\nRead the first user message in the conversation directly.\n\nIF the user message is only a greeting or only A or only B: reply with only the word SKIP.\n\nIF the user message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY):\nBased on the profile and job matches in the conversation provide:\n\n---\n**CAREER RECOMMENDATIONS**\n\n**Skill Gaps**:\n- [skill] - [why important for their target roles]\n- [skill] - [why important]\n- [skill] - [why important]\n\n**Suggested Courses**:\n- [Course Name] on [Platform] - [duration]\n- [Course Name] on [Platform] - [duration]\n- [Course Name] on [Platform] - [duration]\n\n**Career Advice**:\n- [actionable step 1]\n- [actionable step 2]\n- [actionable step 3]\n---\n\nIF the user message contains recruiter job requirements (has words like looking for or hiring or need or require or developer or engineer or manager):\nProvide recruiter hiring advice:\n\n---\n**RECRUITER RECOMMENDATIONS**\n\n**Interview Questions to Ask**:\n- [question 1]\n- [question 2]\n- [question 3]\n\n**Red Flags to Watch For**:\n- [red flag 1]\n- [red flag 2]\n\n**Hiring Tips**:\n- [tip 1]\n- [tip 2]\n- [tip 3]\n---",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      },
      {
        "provider": "autogen_agentchat.agents.AssistantAgent",
        "component_type": "agent",
        "version": 1,
        "component_version": 1,
        "label": "trend_analyzer",
        "config": {
          "name": "trend_analyzer",
          "description": "Final market analysis and summary agent.",
          "system_message": "You are a job market trend analyzer. You are the last agent.\n\nRead the first user message in the conversation directly.\n\nIF the user message is only a greeting or only A or only B: reply with only TERMINATE.\n\nIF the user message contains resume content (has SKILLS or EXPERIENCE or EDUCATION or SUMMARY):\nWrite the final summary:\n\n---\n**=== MARKET ANALYSIS SUMMARY ===**\n\n**1. Most In-Demand Skills from Your Profile**:\n| Skill | Market Demand | Your Level |\n|-------|--------------|------------|\n| [skill] | High/Medium/Low | Present/Missing |\n\n**2. Best Job Roles for You**:\n- [Role]: [why it fits] | Avg Salary: [range]\n\n**3. Recommended Career Direction**:\n[2-3 sentences of strategic advice]\n\n**4. 2025 Market Trends Relevant to You**:\n- [trend 1]\n- [trend 2]\n- [trend 3]\n---\n\nIF the user message contains recruiter job requirements (has words like looking for or hiring or need or require or developer or engineer or manager):\nWrite the final recruiter summary:\n\n---\n**=== RECRUITER MARKET SUMMARY ===**\n\n**1. Market Availability of This Profile**:\n- [how easy or hard it is to find this candidate]\n\n**2. Typical Salary Range to Offer**:\n- [range based on role and skills]\n\n**3. 2025 Market Trends for This Role**:\n- [trend 1]\n- [trend 2]\n- [trend 3]\n\n**4. Hiring Timeline Estimate**:\n- [how long it typically takes to hire for this role]\n---\n\nAlways end with TERMINATE.",
          "reflect_on_tool_use": false,
          "tool_call_summary_format": "{result}",
          "model_client": {
            "provider": "autogen_ext.models.openai.OpenAIChatCompletionClient",
            "component_type": "model",
            "version": 1,
            "component_version": 1,
            "label": "gpt-4o-mini",
            "config": {
              "model": "gpt-4o-mini",
              "api_key": "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",
              "base_url": "https://openrouter.ai/api/v1"
            }
          },
          "tools": []
        }
      }
    ],
    "termination_condition": {
      "provider": "autogen_agentchat.conditions.TextMentionTermination",
      "component_type": "termination",
      "version": 1,
      "component_version": 1,
      "label": "TextMentionTermination",
      "config": {
        "text": "TERMINATE"
      }
    }
  }
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
