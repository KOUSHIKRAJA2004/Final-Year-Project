# Explainable AI-Powered ATS System Architecture

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Candidate   │  │  HR/Admin    │  │  Public API  │          │
│  │  Dashboard   │  │  Dashboard   │  │  (Swagger)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
│                    FastAPI + JWT Auth                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Core ATS    │    │  Explainable │    │  RAG/MCP     │
│  Services    │    │  AI Engine   │    │  Services    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI/ML Processing Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Embeddings  │  │  SHAP/XAI    │  │  LLM (RAG)  │          │
│  │  (Transformers)│  │  Explainer  │  │  (Ollama)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │  Vector DB    │  │  File Store  │          │
│  │  (Structured)│  │  (Embeddings) │  │  (Resumes)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Core Modules Architecture

### 2.1 Backend Services (FastAPI)

```
ats_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Configuration
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py         # JWT authentication
│   │   │   ├── candidates.py   # Candidate endpoints
│   │   │   ├── jobs.py         # Job posting endpoints
│   │   │   ├── analysis.py     # Resume/JD analysis
│   │   │   ├── explainability.py  # XAI explanations
│   │   │   ├── recommendations.py # Course/job recommendations
│   │   │   └── chatbot.py      # RAG chatbot
│   │
│   ├── core/
│   │   ├── ats_engine.py       # Core ATS matching
│   │   ├── explainer.py        # SHAP-based explainer
│   │   ├── embeddings.py       # Sentence transformers
│   │   ├── skill_extractor.py  # Advanced skill extraction
│   │   └── matcher.py          # Semantic matching
│   │
│   ├── services/
│   │   ├── resume_parser.py    # PDF/DOCX parsing
│   │   ├── jd_parser.py        # Job description parsing
│   │   ├── skill_analyzer.py   # Skill gap analysis
│   │   ├── course_recommender.py # Learning path
│   │   ├── salary_predictor.py # Salary prediction
│   │   ├── job_scraper.py      # Job recommendations
│   │   └── linkedin_analyzer.py # LinkedIn optimization
│   │
│   ├── models/
│   │   ├── database.py         # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   │
│   ├── rag/
│   │   ├── vector_store.py     # Vector database
│   │   ├── retriever.py        # RAG retriever
│   │   ├── knowledge_base.py   # ATS knowledge base
│   │   └── mcp_client.py       # Model Context Protocol
│   │
│   └── utils/
│       ├── database.py         # DB connection
│       └── security.py         # JWT, hashing
```

## 3. Database Schema

### 3.1 Core Tables

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    user_type VARCHAR(20) CHECK (user_type IN ('candidate', 'hr', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    file_path VARCHAR(500),
    raw_text TEXT,
    parsed_data JSONB,  -- Structured resume data
    skills JSONB,        -- Extracted skills array
    experience_years DECIMAL(3,1),
    education JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job Descriptions
CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    hr_user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    required_skills JSONB,
    preferred_skills JSONB,
    experience_required DECIMAL(3,1),
    salary_range_min INTEGER,
    salary_range_max INTEGER,
    location VARCHAR(255),
    embedding VECTOR(384),  -- For semantic search
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ATS Match Results
CREATE TABLE ats_matches (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    job_id INTEGER REFERENCES job_descriptions(id),
    overall_score DECIMAL(5,2),  -- 0-100
    skill_match_score DECIMAL(5,2),
    experience_match_score DECIMAL(5,2),
    education_match_score DECIMAL(5,2),
    explanation JSONB,  -- Detailed XAI explanation
    feature_importance JSONB,  -- SHAP values
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skill Gap Analysis
CREATE TABLE skill_gaps (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES ats_matches(id),
    missing_skills JSONB,
    weak_skills JSONB,
    irrelevant_skills JSONB,
    skill_importance_scores JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning Recommendations
CREATE TABLE learning_paths (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    skill_gap_id INTEGER REFERENCES skill_gaps(id),
    skill_name VARCHAR(255),
    course_recommendations JSONB,
    learning_roadmap JSONB,
    expected_score_increase DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Salary Predictions
CREATE TABLE salary_predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    current_skills JSONB,
    predicted_salary_min INTEGER,
    predicted_salary_max INTEGER,
    skill_contributions JSONB,  -- Skill -> salary mapping
    what_if_scenarios JSONB,    -- Future salary with new skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chatbot Conversations (RAG)
CREATE TABLE chatbot_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    session_id VARCHAR(255) UNIQUE,
    context_type VARCHAR(50),  -- 'ats_education', 'resume_analysis', etc.
    context_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector Store (for RAG)
CREATE TABLE knowledge_embeddings (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50),  -- 'ats_guide', 'skill_info', etc.
    content_text TEXT,
    embedding VECTOR(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. API Contracts

### 4.1 Resume + JD Analysis

```python
POST /api/v1/analysis/resume-jd
Request:
{
    "resume_file": File,
    "job_description": str,
    "include_explanation": bool = True
}

Response:
{
    "ats_score": 0-100,
    "breakdown": {
        "skill_match": 0-100,
        "experience_match": 0-100,
        "education_match": 0-100
    },
    "explanation": {
        "missing_skills": [
            {
                "skill": "Python",
                "importance": 0.85,
                "reason": "Required in JD but not found in resume",
                "expected_impact": "+15 points if added"
            }
        ],
        "weak_skills": [...],
        "irrelevant_skills": [...],
        "feature_importance": {
            "python": 0.25,
            "experience_years": 0.20,
            ...
        }
    },
    "recommendations": {
        "priority_skills": [...],
        "courses": [...],
        "expected_score_improvement": 25
    }
}
```

### 4.2 Explainable AI Endpoint

```python
GET /api/v1/explainability/match/{match_id}
Response:
{
    "match_id": 123,
    "overall_score": 72.5,
    "explanations": {
        "why_rejected": [
            "Missing critical skill: Python (weight: 0.25)",
            "Experience gap: Required 3+ years, resume shows 1 year",
            "Education mismatch: JD requires CS degree, resume shows Business"
        ],
        "why_accepted": [
            "Strong match in JavaScript (0.20 weight)",
            "Relevant project experience in React"
        ],
        "feature_attributions": {
            "python": -15.5,  // Negative = missing
            "javascript": +12.3,  // Positive = present
            "experience_years": -8.2
        },
        "shap_values": {...}
    }
}
```

### 4.3 RAG Chatbot

```python
POST /api/v1/chatbot/ats-education
Request:
{
    "question": "Why was my resume rejected?",
    "context": {
        "resume_id": 123,
        "job_id": 456
    },
    "session_id": "uuid"
}

Response:
{
    "answer": "Based on your resume analysis...",
    "sources": [
        {"type": "ats_guide", "content": "..."},
        {"type": "skill_info", "content": "..."}
    ],
    "confidence": 0.92
}
```

## 5. Technology Stack

### Backend
- **FastAPI**: Modern async Python framework
- **SQLAlchemy**: ORM
- **PostgreSQL**: Primary database
- **pgvector**: Vector similarity search
- **Sentence Transformers**: Embeddings
- **SHAP**: Explainable AI
- **Ollama/OpenAI**: LLM for RAG

### AI/ML
- **spaCy**: NLP processing
- **Transformers**: BERT/RoBERTa embeddings
- **SHAP**: Feature attribution
- **scikit-learn**: ML models

### Frontend (Future)
- **Next.js**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Recharts**: Visualizations

## 6. Explainability Strategy

1. **Feature Importance**: SHAP values for each skill/feature
2. **Natural Language Explanations**: LLM-generated explanations
3. **Visual Explanations**: Charts showing score breakdown
4. **What-If Analysis**: Show score changes with skill additions
5. **Rule-Based Explanations**: Clear rules (e.g., "Python required but missing")

## 7. RAG Implementation

- **Knowledge Base**: ATS guides, skill descriptions, industry standards
- **Vector Store**: pgvector for semantic search
- **Retrieval**: Top-K similar chunks
- **Generation**: LLM (Ollama) with retrieved context
- **MCP**: Model Context Protocol for structured tool calling

