from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.core.utils import get_current_time

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    user_type = Column(String, default="candidate")  # candidate, hr, admin
    created_at = Column(DateTime, default=get_current_time)
    
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    jobs = relationship("JobDescription", back_populates="hr_user", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)
    raw_text = Column(Text)
    parsed_data = Column(JSON)  # Name, contact, etc.
    skills = Column(JSON)       # List of skills
    experience_years = Column(Integer) # Simplified to Int for now, or Float
    education = Column(JSON)
    created_at = Column(DateTime, default=get_current_time)

    user = relationship("User", back_populates="resumes")
    matches = relationship("MatchResult", back_populates="resume", cascade="all, delete-orphan")
