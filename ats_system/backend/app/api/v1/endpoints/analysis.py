from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import shutil
import os
import uuid

from app.services.ai.parser import ResumeParser
from app.services.ai.matcher import MatcherEngine
from app.services.ai.explainer import ExplainabilityEngine

router = APIRouter()

parser = ResumeParser()
matcher = MatcherEngine()
explainer = ExplainabilityEngine()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyzes a resume against a job description.
    Returns match score, skill gaps, and explanations.
    """
    # 1. Save file temporarily
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Parse Resume
        resume_data = parser.parse(file_path)
        
        # 3. Process JD (Simple extraction for now)
        # ideally we use a JD Parser, but for now we treat it as raw text
        jd_data = {
            "description": job_description,
            "required_skills": parser.extract_skills(job_description.lower()) # reusing skill extractor
        }

        # 4. Compute Match
        match_result = matcher.compute_match(resume_data, jd_data)

        # 5. Explain
        explanation = explainer.explain_match(resume_data, jd_data, match_result)

        return {
            "match_score": match_result["overall_score"],
            "breakdown": match_result,
            "explanation": explanation,
            "extracted_data": {
                "resume_skills": resume_data.get("skills"),
                "jd_skills": jd_data.get("required_skills")
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
