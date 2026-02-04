from typing import Dict, List, Any

class ExplainabilityEngine:
    def __init__(self):
        pass

    def explain_match(self, resume_data: dict, jd_data: dict, match_details: dict) -> dict:
        """
        Generates human-readable explanations for the match score.
        """
        explanation = {
            "summary": "",
            "missing_skills": [],
            "score_breakdown": match_details,
            "suggestions": []
        }

        # 1. Analyze Skills
        resume_skills = set(resume_data.get("skills", []))
        jd_skills = set(jd_data.get("required_skills", []))
        
        missing = []
        if jd_skills:
            missing = list(jd_skills - resume_skills)
        
        explanation["missing_skills"] = missing

        # 2. Generate Summary
        score = match_details.get("overall_score", 0)
        if score >= 80:
            explanation["summary"] = "Excellent match! Your resume strongly aligns with the job description."
        elif score >= 50:
            explanation["summary"] = "Good match, but there are some critical skills missing."
        else:
            explanation["summary"] = "Low match. You are missing several key requirements for this role."

        # 3. Generate Suggestions
        if missing:
            explanation["suggestions"].append(
                f"Consider adding the following skills to your resume or learning them: {', '.join(missing[:5])}"
            )
        
        if match_details.get("embeddings_match", 0) < 50:
             explanation["suggestions"].append(
                 "Your resume content/keywords might not semantically align with the job description's language. Try to use similar terminology."
             )

        return explanation
