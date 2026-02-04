import numpy as np
try:
    from sentence_transformers import SentenceTransformer, util
    from sklearn.metrics.pairwise import cosine_similarity
    MODEL_NAME = 'all-MiniLM-L6-v2'
except ImportError:
    SentenceTransformer = None
    cosine_similarity = None

class MatcherEngine:
    def __init__(self):
        self.model = None
        if SentenceTransformer:
            try:
                # Load model
                self.model = SentenceTransformer(MODEL_NAME)
                print(f"Loaded SentenceTransformer: {MODEL_NAME}")
            except Exception as e:
                print(f"Failed to load SentenceTransformer: {e}")
        else:
            print("sentence-transformers not installed, using fallback.")

    def compute_match(self, resume_data: dict, jd_data: dict) -> dict:
        """
        Computes the match score using hybrid approach:
        1. Keyword Overlap (Skills)
        2. Semantic Similarity (Embeddings)
        """
        resume_text = resume_data.get("raw_text", "")
        jd_text = jd_data.get("description", "")
        
        # 1. Skill Match Score
        resume_skills = set(resume_data.get("skills", []))
        # JD skills might be a list or we might need to extract them if not provided
        # For this prototype, assume we have a list of required skills or extract from text
        jd_skills = set(jd_data.get("required_skills", []))
        
        skill_score = 0.0
        if jd_skills:
            intersection = resume_skills.intersection(jd_skills)
            skill_score = (len(intersection) / len(jd_skills)) * 100
        else:
            # If JD skills not explicit, extracting them locally would be ideal
            # Fallback: assume all resume skills found in JD text are relevant
            pass 

        # 2. Semantic Score
        semantic_score = 0.0
        if self.model and resume_text and jd_text:
            try:
                emb1 = self.model.encode(resume_text, convert_to_tensor=True)
                emb2 = self.model.encode(jd_text, convert_to_tensor=True)
                # Compute cosine similarity
                semantic_score = util.cos_sim(emb1, emb2).item() * 100
            except Exception as e:
                print(f"Embedding error: {e}")
        
        # Weighted Average
        # 60% Skills, 40% Semantic (if available)
        if self.model:
            final_score = (skill_score * 0.6) + (semantic_score * 0.4)
        else:
            final_score = skill_score

        return {
            "overall_score": round(final_score, 2),
            "skill_match": round(skill_score, 2),
            "embeddings_match": round(semantic_score, 2)
        }
