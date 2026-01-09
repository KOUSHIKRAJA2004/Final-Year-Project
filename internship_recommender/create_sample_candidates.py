"""
Script to create 15 sample candidates with diverse profiles
Run this script to populate the database with test candidates
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import db

# Sample candidates data
CANDIDATES = [
    {
        "username": "rakesh",
        "email": "rakesh@email.com",
        "password": "password123",
        "full_name": "Rakesh",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Python, Django, REST API, SQL, PostgreSQL, Git, Linux, Docker"
    },
    {
        "username": "sneha",
        "email": "sneha@email.com",
        "password": "password123",
        "full_name": "Sneha",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Information Technology",
        "skills": "Java, Spring Boot, MySQL, JavaScript, React, HTML, CSS, AWS"
    },
    {
        "username": "ram",
        "email": "ram@email.com",
        "password": "password123",
        "full_name": "Ram",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Python, Machine Learning, TensorFlow, Pandas, NumPy, Jupyter, Data Visualization, Statistics"
    },
    {
        "username": "priya",
        "email": "priya@email.com",
        "password": "password123",
        "full_name": "Priya",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "JavaScript, React, Node.js, MongoDB, Express, TypeScript, Redux, HTML, CSS"
    },
    {
        "username": "arjun",
        "email": "arjun@email.com",
        "password": "password123",
        "full_name": "Arjun",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Electronics",
        "skills": "C++, Embedded Systems, IoT, Arduino, Raspberry Pi, Python, Linux, Microcontrollers"
    },
    {
        "username": "kavya",
        "email": "kavya@email.com",
        "password": "password123",
        "full_name": "Kavya",
        "degree": "B.Sc",
        "study_year": 3,
        "sector": "Data Science",
        "stream": "Data Science",
        "skills": "Python, R, SQL, Tableau, Power BI, Excel, Statistics, Machine Learning, Data Analysis"
    },
    {
        "username": "sam",
        "email": "sam@email.com",
        "password": "password123",
        "full_name": "Sam",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Python, Flask, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, CI/CD, Microservices"
    },
    {
        "username": "ananya",
        "email": "ananya@email.com",
        "password": "password123",
        "full_name": "Ananya",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Information Technology",
        "skills": "Java, Spring Framework, Hibernate, REST API, MySQL, Maven, Git, JUnit, Agile"
    },
    {
        "username": "vishal",
        "email": "vishal@email.com",
        "password": "password123",
        "full_name": "Vishal",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Python, Django, React, PostgreSQL, Docker, AWS, Terraform, Jenkins, Linux"
    },
    {
        "username": "meera",
        "email": "meera@email.com",
        "password": "password123",
        "full_name": "Meera",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "JavaScript, Vue.js, Node.js, MongoDB, Express, GraphQL, TypeScript, Jest, Webpack"
    },
    {
        "username": "raj",
        "email": "raj@email.com",
        "password": "password123",
        "full_name": "Raj",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "C#, .NET, ASP.NET, SQL Server, Entity Framework, Azure, Git, Unit Testing, Design Patterns"
    },
    {
        "username": "divya",
        "email": "divya@email.com",
        "password": "password123",
        "full_name": "Divya",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Information Technology",
        "skills": "Python, Data Science, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Jupyter, SQL"
    },
    {
        "username": "kiran",
        "email": "kiran@email.com",
        "password": "password123",
        "full_name": "Kiran",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Go, Kubernetes, Docker, Microservices, REST API, PostgreSQL, Redis, gRPC, Linux"
    },
    {
        "username": "neha",
        "email": "neha@email.com",
        "password": "password123",
        "full_name": "Neha",
        "degree": "B.Tech",
        "study_year": 3,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "React Native, Flutter, iOS, Android, JavaScript, TypeScript, Redux, Firebase, REST API"
    },
    {
        "username": "aditya",
        "email": "aditya@email.com",
        "password": "password123",
        "full_name": "Aditya",
        "degree": "B.Tech",
        "study_year": 4,
        "sector": "Technology",
        "stream": "Computer Science",
        "skills": "Python, Machine Learning, Deep Learning, PyTorch, TensorFlow, Computer Vision, NLP, OpenCV, Pandas"
    }
]

def create_sample_candidates():
    """Create sample candidates in the database"""
    print("Creating sample candidates...")
    print("=" * 50)
    
    created_count = 0
    skipped_count = 0
    
    for candidate_data in CANDIDATES:
        username = candidate_data["username"]
        email = candidate_data["email"]
        password = candidate_data["password"]
        full_name = candidate_data["full_name"]
        
        # Check if user already exists
        existing_user = db.get_user_by_username(username)
        if existing_user:
            print(f"[SKIP] Skipping {username} - already exists")
            skipped_count += 1
            continue
        
        # Create user
        success = db.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            user_role='student'
        )
        
        if success:
            # Get the created user
            user = db.get_user_by_username(username)
            if user:
                # Create profile
                profile_data = {
                    'degree': candidate_data.get('degree'),
                    'study_year': candidate_data.get('study_year'),
                    'sector': candidate_data.get('sector'),
                    'stream': candidate_data.get('stream'),
                    'skills': candidate_data.get('skills')
                }
                
                db.update_user_profile(user['id'], profile_data)
                print(f"[OK] Created: {full_name} ({username}) - {candidate_data.get('stream')}")
                created_count += 1
            else:
                print(f"[ERROR] Failed to create profile for {username}")
        else:
            print(f"[ERROR] Failed to create user {username}")
    
    print("=" * 50)
    print(f"\nSummary:")
    print(f"   Created: {created_count} candidates")
    print(f"   Skipped: {skipped_count} candidates (already exist)")
    print(f"   Total: {len(CANDIDATES)} candidates")
    print("\nSample candidates created successfully!")
    print("\nYou can now:")
    print("   1. Login as HR user")
    print("   2. Create a job posting")
    print("   3. Use the HR dashboard to analyze and find suitable candidates")

if __name__ == "__main__":
    try:
        create_sample_candidates()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

