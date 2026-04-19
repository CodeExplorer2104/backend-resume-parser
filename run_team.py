import asyncio
import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
)

def call_api(resume):
    try:
        r = requests.post("http://127.0.0.1:8000/match", json={"resume": resume}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e), "parsed_data": {}, "matched_jobs": [], "recommendations": ""}

def add_job(job):
    try:
        r = requests.post("http://127.0.0.1:8000/add_job", json={"job": job}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

async def run_agents(resume_text):
    api_result = call_api(resume_text)

    resume_parser = AssistantAgent(
        name="resume_parser",
        model_client=model_client,
        system_message="You are a resume parser. No emojis. Parse the resume in the task and display clearly: Name, Skills, Experience, Projects, Education. End with DONE."
    )
    structurer = AssistantAgent(
        name="structurer",
        model_client=model_client,
        system_message="You are a data structurer. No emojis. Format resume data from conversation into clean sections: Skills | Work Experience | Projects | Education. End with DONE."
    )
    matcher = AssistantAgent(
        name="matcher",
        model_client=model_client,
        system_message="You are a job matcher. No emojis. Use matched_jobs from the task data. Display ranked list with job title and score. If unavailable, suggest 3 roles based on skills. End with DONE."
    )
    recommender = AssistantAgent(
        name="recommender",
        model_client=model_client,
        system_message="You are a career recommender. No emojis. Use recommendations from the task data. Display: Skill Gaps | Suggested Courses | Career Advice. End with DONE."
    )
    trend_analyzer = AssistantAgent(
        name="trend_analyzer",
        model_client=model_client,
        system_message="You are a market analyst. No emojis. Write final summary: 1) Top in-demand skills 2) Best roles for candidate 3) Career direction 4) 2025 market trends. End with TERMINATE."
    )

    task = f"""Resume:
{resume_text}

API Data:
Parsed: {api_result.get('parsed_data', 'N/A')}
Matched Jobs: {api_result.get('matched_jobs', 'N/A')}
Recommendations: {api_result.get('recommendations', 'N/A')}
"""

    team = RoundRobinGroupChat(
        participants=[resume_parser, structurer, matcher, recommender, trend_analyzer],
        termination_condition=TextMentionTermination("TERMINATE")
    )

    print("\n" + "="*50)
    print("PROCESSING RESUME")
    print("="*50)

    async for message in team.run_stream(task=task):
        if hasattr(message, 'source') and hasattr(message, 'content'):
            print(f"\n[{message.source.upper()}]")
            print(message.content)
            print("-"*40)

async def main():
    print("\n" + "="*50)
    print("  RESUME MATCHING SYSTEM")
    print("="*50)
    print("\n[A] Applicant - Looking for jobs")
    print("[B] Recruiter - Hiring someone")

    choice = input("\nEnter A or B: ").strip().upper()

    if choice == "A":
        print("\nOptions:")
        print("1. Full analysis (parse + match + recommendations + trends)")
        print("2. Job matching only")
        print("3. Career recommendations only")
        input("\nPress Enter to continue... ")

        print("\nPaste your resume. Type END on a new line when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        resume_text = "\n".join(lines).strip()
        if not resume_text:
            print("No resume entered.")
            return

        await run_agents(resume_text)

    elif choice == "B":
        print("\nEnter the job role and required skills:")
        print("Example: Python ML Engineer with TensorFlow and Docker\n")
        requirements = input("Requirements: ").strip()

        result = add_job(requirements)
        if "error" in result:
            print(f"Could not add job: {result['error']}")
            print("Make sure backend is running: uvicorn main:app --reload --port 8000")
        else:
            print(f"Job added: {result}")

    else:
        print("Invalid. Run again and type A or B.")

asyncio.run(main())