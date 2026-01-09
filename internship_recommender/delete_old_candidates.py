"""
Script to delete old candidates with Western names from the database
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import db

# Old candidate usernames to delete
OLD_CANDIDATES = [
    "john_doe",
    "sarah_smith",
    "mike_johnson",
    "emily_williams",
    "david_brown",
    "lisa_anderson",
    "robert_taylor",
    "jennifer_martinez",
    "william_davis",
    "amanda_wilson",
    "james_moore",
    "patricia_thomas",
    "richard_jackson",
    "linda_white",
    "charles_harris"
]

def delete_old_candidates():
    """Delete old candidates with Western names from the database"""
    print("Deleting old candidates with Western names...")
    print("=" * 50)
    
    deleted_count = 0
    not_found_count = 0
    
    cursor = None
    try:
        cursor = db._get_cursor()
        placeholder = db._get_placeholder()
        
        for username in OLD_CANDIDATES:
            # First, get the user ID
            user = db.get_user_by_username(username)
            
            if user:
                user_id = user['id']
                
                # Delete user (cascade will delete profile and related data)
                cursor.execute(f"DELETE FROM users WHERE id = {placeholder}", (user_id,))
                db.connection.commit()
                
                print(f"[DELETED] {username} (ID: {user_id})")
                deleted_count += 1
            else:
                print(f"[NOT FOUND] {username} - already deleted or doesn't exist")
                not_found_count += 1
        
        print("=" * 50)
        print(f"\nSummary:")
        print(f"   Deleted: {deleted_count} candidates")
        print(f"   Not Found: {not_found_count} candidates")
        print(f"   Total Processed: {len(OLD_CANDIDATES)} candidates")
        print("\nOld candidates deleted successfully!")
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    try:
        delete_old_candidates()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

