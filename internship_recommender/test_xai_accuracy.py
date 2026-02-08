
import sys
import os
import pandas as pd
import numpy as np

# Force UTF-8 for stdout
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add the current directory to sys.path so we can import utils
sys.path.append(os.getcwd())

from utils.xai_explainer import get_salary_explainer
from utils.salary_predictor import ensure_trained_model

def test_xai_accuracy():
    print("--- Testing XAI Accuracy ---")
    
    # 1. Ensure Model Exists
    print("1. Checking Model...")
    ensure_trained_model()
    
    # 2. Initialize Explainer
    print("2. Initializing Explainer...")
    try:
        explainer = get_salary_explainer()
        if not explainer.model:
            print("ERROR: Model failed to load in explainer.")
            return
        print("   Explainer initialized successfully.")
    except Exception as e:
        print(f"ERROR: Failed to initialize explainer: {e}")
        return

    # 3. Define Test Cases
    test_cases = [
        {
            "role": "Python Developer",
            "skills": ["Python", "Django", "SQL", "Git", "REST API"],
            "experience": 2
        },
        {
            "role": "Data Scientist",
            "skills": ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Tableau"],
            "experience": 4
        },
        {
            "role": "Intern", 
            "skills": ["Python"],
            "experience": 0
        }
    ]

    # 4. Run Tests
    for i, test in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {test['role']} ({test['experience']} yrs exp) ---")
        
        try:
            # Predict & Explain
            result = explainer.explain_prediction(
                skills=test['skills'],
                role=test['role'],
                experience_years=test['experience']
            )
            
            # 5. Validate Output Structure
            pred_salary = result.get('predicted_salary', 0)
            explanation = result.get('explanation', '')
            contributions = result.get('feature_contributions', {})
            
            print(f"   Predicted Salary: ₹{pred_salary:,.2f}")
            print(f"   Explanation Text: \n{explanation}")
            
            print("\n   Feature Contributions:")
            total_contribution_pct = 0
            for feature, data in contributions.items():
                pct = data.get('contribution_pct', 0)
                total_contribution_pct += pct
                print(f"     - {feature}: {pct:.2f}%")
            
            # 6. Sanity Checks
            if pred_salary <= 0:
                print("   [WARNING] Predicted salary is 0 or negative.")
            else:
                print("   [PASS] Predicted salary is positive.")
                
            if not explanation:
                print("   [WARNING] No explanation text generated.")
            else:
                print("   [PASS] Explanation text generated.")
                
            if not contributions:
                print("   [WARNING] No feature contributions found.")
            else:
                print("   [PASS] Feature contributions calculated.")

            # Check logic consistency
            # In the approximation method, contributions might not sum exactly to 100% of prediction due to base intercept,
            # but we can check if the relative ordering makes sense (e.g. higher experience should usually contribute more).
            
        except Exception as e:
            print(f"   [ERROR] Test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_xai_accuracy()
