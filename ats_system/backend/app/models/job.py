from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.core.utils import get_current_time

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    hr_user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    required_skills = Column(JSON)
    preferred_skills = Column(JSON)
    experience_required = Column(Integer)
    location = Column(String)
    created_at = Column(DateTime, default=get_current_time)

    hr_user = relationship("User", back_populates="jobs")
    matches = relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    overall_score = Column(Integer) # 0-100
    explanation = Column(JSON)      # Detailed XAI output
    created_at = Column(DateTime, default=get_current_time)

    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobDescription", back_populates="matches")
