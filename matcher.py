import faiss
import numpy as np
from embedding import get_embedding

# Use cosine similarity (better for text)
index = faiss.IndexFlatIP(384)

job_data = []  # stores full job info


def add_job(job_desc):
    vec = get_embedding(job_desc)
    index.add(np.array([vec]))
    
    job_data.append({
        "description": job_desc
    })


def compute_skill_score(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    common = resume_words.intersection(job_words)
    
    if len(job_words) == 0:
        return 0
    
    return len(common) / len(job_words)


def match_resume(resume_text):
    vec = get_embedding(resume_text)

    D, I = index.search(np.array([vec]), k=3)

    results = []

    for idx, score in zip(I[0], D[0]):
        if idx < len(job_data):

            job_desc = job_data[idx]["description"]

            # Skill-based score
            skill_score = compute_skill_score(resume_text, job_desc)

            # Final score (weighted)
            final_score = (0.7 * float(score)) + (0.3 * skill_score)

            results.append({
                "job": job_desc,
                "similarity_score": float(score),
                "skill_score": skill_score,
                "final_score": final_score
            })

    # Sort by final score
    results = sorted(results, key=lambda x: x["final_score"], reverse=True)

    return results