"""
Script to create sample job postings for HR
Run this script to populate the database with test job postings
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import db

# Sample job postings data
JOB_POSTINGS = [
    {
        "title": "Python Developer",
        "description": "We are looking for a skilled Python Developer to join our team. The ideal candidate should have experience with web frameworks, REST APIs, and database management. You will work on developing scalable backend services and APIs.",
        "required_skills": "Python, Django, REST API, SQL, PostgreSQL, Git, Linux",
        "location": "Bangalore, India",
        "salary_low": 400000,
        "salary_high": 800000
    },
    {
        "title": "Full Stack Developer",
        "description": "Join our team as a Full Stack Developer. You'll work on both frontend and backend development, building modern web applications. Experience with React, Node.js, and databases is essential.",
        "required_skills": "JavaScript, React, Node.js, MongoDB, Express, HTML, CSS, REST API",
        "location": "Mumbai, India",
        "salary_low": 500000,
        "salary_high": 900000
    },
    {
        "title": "Machine Learning Engineer",
        "description": "We're seeking a Machine Learning Engineer to develop and deploy ML models. The role involves working with large datasets, building predictive models, and implementing deep learning solutions.",
        "required_skills": "Python, Machine Learning, TensorFlow, Pandas, NumPy, Data Science, Statistics",
        "location": "Hyderabad, India",
        "salary_low": 600000,
        "salary_high": 1200000
    },
    {
        "title": "Java Backend Developer",
        "description": "Looking for an experienced Java Developer to build robust backend systems. You should be proficient in Spring Framework, REST APIs, and database design. Experience with microservices architecture is a plus.",
        "required_skills": "Java, Spring Boot, Spring Framework, MySQL, REST API, Hibernate, Maven",
        "location": "Pune, India",
        "salary_low": 450000,
        "salary_high": 850000
    },
    {
        "title": "Data Scientist",
        "description": "We need a Data Scientist to analyze complex datasets and build predictive models. The role requires strong statistical knowledge, data visualization skills, and experience with machine learning tools.",
        "required_skills": "Python, R, SQL, Data Science, Statistics, Machine Learning, Tableau, Pandas",
        "location": "Delhi, India",
        "salary_low": 550000,
        "salary_high": 1000000
    },
    {
        "title": "DevOps Engineer",
        "description": "Join our DevOps team to manage cloud infrastructure, CI/CD pipelines, and containerization. Experience with Docker, Kubernetes, and cloud platforms is required.",
        "required_skills": "Docker, Kubernetes, CI/CD, AWS, Linux, Terraform, Jenkins, Microservices",
        "location": "Chennai, India",
        "salary_low": 500000,
        "salary_high": 950000
    },
    {
        "title": "Mobile App Developer",
        "description": "We're looking for a Mobile App Developer to build cross-platform mobile applications. Experience with React Native or Flutter is essential, along with knowledge of mobile UI/UX principles.",
        "required_skills": "React Native, Flutter, JavaScript, TypeScript, Mobile Development, REST API, Firebase",
        "location": "Bangalore, India",
        "salary_low": 400000,
        "salary_high": 800000
    },
    {
        "title": "Frontend Developer",
        "description": "Seeking a Frontend Developer to create beautiful and responsive web interfaces. You should be proficient in modern JavaScript frameworks, CSS, and have a good eye for design.",
        "required_skills": "JavaScript, React, Vue.js, HTML, CSS, TypeScript, Redux, Webpack",
        "location": "Mumbai, India",
        "salary_low": 350000,
        "salary_high": 700000
    }
]

def create_sample_jobs():
    """Create sample job postings in the database"""
    print("Creating sample job postings...")
    print("=" * 50)
    
    # Get or create an HR user
    hr_user = db.get_user_by_username("admin")
    if not hr_user:
        # Create a default HR user
        print("Creating default HR user (admin)...")
        db.create_user("admin", "admin@talentmatch.com", "admin123", "HR Admin", "hr")
        hr_user = db.get_user_by_username("admin")
    
    if not hr_user or hr_user.get('user_role') != 'hr':
        print("[ERROR] No HR user found. Please create an HR user first.")
        print("You can use /promote-to-hr to promote a user to HR role.")
        return
    
    hr_user_id = hr_user['id']
    created_count = 0
    skipped_count = 0
    
    for job_data in JOB_POSTINGS:
        title = job_data["title"]
        
        # Check if job already exists
        existing_jobs = db.get_job_postings(hr_user_id=hr_user_id)
        job_exists = any(job.get('title') == title for job in existing_jobs)
        
        if job_exists:
            print(f"[SKIP] Skipping {title} - already exists")
            skipped_count += 1
            continue
        
        # Create job posting
        job_id = db.create_job_posting(
            hr_user_id=hr_user_id,
            title=job_data["title"],
            description=job_data["description"],
            required_skills=job_data["required_skills"],
            location=job_data["location"],
            salary_range_low=job_data.get("salary_low"),
            salary_range_high=job_data.get("salary_high")
        )
        
        if job_id:
            print(f"[OK] Created: {title} - {job_data['location']}")
            created_count += 1
        else:
            print(f"[ERROR] Failed to create job: {title}")
    
    print("=" * 50)
    print(f"\nSummary:")
    print(f"   Created: {created_count} job postings")
    print(f"   Skipped: {skipped_count} job postings (already exist)")
    print(f"   Total: {len(JOB_POSTINGS)} job postings")
    print("\nJob postings created successfully!")
    print("\nYou can now:")
    print("   1. Login as HR user (admin/admin123)")
    print("   2. Go to HR Dashboard")
    print("   3. Select a job posting from the dropdown")
    print("   4. View AI-powered candidate analysis and matching")

if __name__ == "__main__":
    try:
        create_sample_jobs()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

