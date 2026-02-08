# Application Workflow & Architecture

This document provides a visual overview of the Internship Recommender System, including user flows, system architecture, and AI integration points.

## 1. System Architecture

The application follows a standard Model-View-Controller (MVC) pattern adapted for Flask.

```mermaid
graph TD
    Client[Client Browser] <-->|HTTP/HTTPS| Flask[Flask Application]
    
    subgraph "Backend (Flask)"
        Auth[Authentication Module]
        Routes[Route Handlers]
        
        subgraph "AI Services"
            Gemini[Gemini Service]
            Ollama[Ollama Service]
            XAI[XAI Explainer]
            RecSys[Recommendation Engine]
        end
        
        DB_Ops[Database Operations]
    end
    
    subgraph "Data Storage"
        SQLite[(SQLite Database)]
        FS[File System]
    end
    
    Flask <--> DB_Ops
    DB_Ops <--> SQLite
    Flask <--> FS
    Routes --> AI_Services
```

## 2. Authentication & User Roles

```mermaid
sequenceDiagram
    participant User
    participant App
    participant DB
    
    User->>App: Access Login/Register
    alt Register
        User->>App: Submit Details (Role: Candidate/HR)
        App->>DB: Create User
        DB-->>App: Success
    else Login
        User->>App: Submit Credentials
        App->>DB: Validate User
        DB-->>App: User Data
    end
    
    alt Role == Candidate
        App-->>User: Redirect to Candidate Dashboard
    else Role == HR
        App-->>User: Redirect to HR Dashboard
    end
```

## 3. Candidate Workflow

Comprehensive flow for a candidate user, from profile creation to job application.

```mermaid
graph TD
    Start[Candidate Dashboard]
    
    Start --> Profile[Profile Management]
    Start --> Resume[Resume Operations]
    Start --> Jobs[Job/Internship Search]
    Start --> Insight[AI Insights]
    
    Profile --> Edit[Edit Profile]
    Profile --> View[View Profile]
    
    Resume --> Upload[Upload Resume]
    Upload --> |OCR & Analysis| Gemini[Gemini AI]
    Gemini --> |Parsed Data| AutoFill[Auto-fill Profile]
    Resume --> Enhance[Resume AI Enhancer]
    
    Jobs --> Recs[View Recommendations]
    Jobs --> Search[Search Internships]
    Recs --> |XAI| Explain[View Explanation]
    Search --> Apply[Apply for Role]
    
    Insight --> Salary[Salary Predictor]
    Insight --> Skills[Skill Gap Analysis]
    Insight --> Chat[ATS Educator Chat]
    
    Salary --> |Input| Model[Prediction Model]
    Model --> |Output| Pred[Prediction & XAI Explanation]
```

## 4. HR Workflow

Flow for HR users to manage jobs and candidates.

```mermaid
graph TD
    HR[HR Dashboard]
    
    HR --> Post[Post New Job]
    HR --> Manage[Manage Jobs]
    HR --> Candidates[Candidate Search]
    
    Post --> DB[(Database)]
    
    Candidates --> View[View Candidate Profile]
    View --> Match[Match with Job]
    Match --> AI_Match[AI Matching Score]
    AI_Match --> Insight[Matching Insights]
    
    HR --> Chat[HR Assistant Chatbot]
    Chat --> Support[Operational Support]
```

## 5. XAI & AI Integration Pipeline

Detailing how the Explainable AI (XAI) and other AI components function.

```mermaid
sequenceDiagram
    participant User
    participant Route
    participant XAI_Engine
    participant Models
    
    Note over User, Models: Scenario: Salary Prediction with Explanation
    
    User->>Route: Request Salary Prediction (Skills, Exp, Role)
    Route->>Models: Predict Salary
    Models-->>Route: Return Prediction
    
    Route->>XAI_Engine: Generate Explanation
    XAI_Engine->>Models: Calculate SHAP Values / Feature Importance
    Models-->>XAI_Engine: Return Values
    XAI_Engine->>XAI_Engine: Generate Human-Readable Text
    XAI_Engine-->>Route: Return Logic & Text
    
    Route-->>User: Display Prediction + "Why?"
```

## 6. Resume Enhancement Flow

```mermaid
stateDiagram-v2
    [*] --> Upload
    Upload --> Analysis: Submit PDF
    Analysis --> Generation: AI Analyzes Content
    Generation --> Review: Suggest Improvements
    Review --> Apply: User Selects Changes
    Apply --> Download: Generate New PDF
    Download --> [*]
```
