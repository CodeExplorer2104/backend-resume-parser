from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from parser import parse_resume
from matcher import match_resume, add_job
from gemini_utils import get_recommendations

@asynccontextmanager
async def lifespan(app: FastAPI):
    add_job("Looking for Python developer with Machine Learning experience")
    add_job("Frontend developer with React and JavaScript")
    add_job("Computer Vision engineer with OpenCV and YOLO")
    yield

app = FastAPI(title="Resume Matching API", lifespan=lifespan)

class ResumeRequest(BaseModel):
    resume: str

class JobRequest(BaseModel):
    job: str

@app.post("/match")
def match(data: ResumeRequest):
    resume = data.resume
    parsed = parse_resume(resume)
    matches = match_resume(resume)
    recommendations = get_recommendations(parsed)
    return {
        "parsed_data": parsed,
        "matched_jobs": matches,
        "recommendations": recommendations
    }

@app.post("/add_job")
def add_new_job(data: JobRequest):
    add_job(data.job)
    return {"message": "Job added successfully"}

@app.get("/")
def root():
    return {"status": "API is running"}