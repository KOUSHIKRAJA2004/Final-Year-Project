import re
import os
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# Common Tech Skills Database (Small subset for prototype)
COMMON_SKILLS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "react", "angular", "vue",
    "node.js", "django", "flask", "fastapi", "spring", "sql", "mysql", "postgresql", "mongodb",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux", "jenkins", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power bi", "excel",
    "communication", "teamwork", "leadership", "problem solving", "agile", "scrum"
}

class ResumeParser:
    def __init__(self):
        pass

    def parse(self, file_path: str, raw_text: str = None) -> dict:
        """
        Parses a resume file or raw text to extract skills, experience, etc.
        """
        text = raw_text
        if not text and file_path:
            text = self._read_file(file_path)
        
        if not text:
            return {"raw_text": "", "skills": [], "email": None, "phone": None}

        # Normalize text
        text_lower = text.lower()
        
        return {
            "raw_text": text,
            "skills": self.extract_skills(text_lower),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "experience_years": self.extract_experience(text_lower)
        }
    
    def _read_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return ""
        
        if file_path.endswith('.pdf'):
            if PdfReader:
                try:
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
                except Exception as e:
                    print(f"Error reading PDF: {e}")
                    return ""
            else:
                print("pypdf not installed")
                return ""
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def extract_skills(self, text: str) -> list:
        # Simple keyword matching against database
        found_skills = []
        words = set(re.findall(r"\b[\w\+\.#]+\b", text))
        
        for skill in COMMON_SKILLS:
            # Handle skills with spaces (e.g. "problem solving")
            if " " in skill:
                if skill in text:
                    found_skills.append(skill)
            else:
                if skill in words:
                    found_skills.append(skill)
        
        return list(set(found_skills))

    def extract_email(self, text: str) -> str:
        if not text: return None
        emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
        return emails[0] if emails else None

    def extract_phone(self, text: str) -> str:
        # Simple regex for phone numbers
        phones = re.findall(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        return phones[0] if phones else None

    def extract_experience(self, text: str) -> float:
        # Heuristic: Find "X years" or "Experience" patterns
        # Very naive implementation
        years_matches = re.findall(r"(\d+)\+?\s*years?", text)
        if years_matches:
            try:
                # return max to be generous
                return max([float(y) for y in years_matches if y.isdigit()])
            except:
                pass
        return 0.0
