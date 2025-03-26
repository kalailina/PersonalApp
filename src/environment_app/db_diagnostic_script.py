import os
import sqlite3
import sys

def diagnose_database():
    # Path to the database
    db_path = "/Users/linakalai/Desktop/UCL/PersonalApp/src/environment_app/instance/environment.db"
    
    print("Diagnostic Information:")
    print("=" * 30)
    
    # Check file existence
    print(f"Database file exists: {os.path.exists(db_path)}")
    
    if os.path.exists(db_path):
        # Check file permissions
        file_stat = os.stat(db_path)
        print(f"File permissions: {oct(file_stat.st_mode)[-3:]}")
        print(f"File size: {file_stat.st_size} bytes")
        
        # Try to connect to the database
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("\nTables in the database:")
            for table in tables:
                print(f"- {table[0]}")
                
                # Count rows in each table
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM '{table[0]}'")
                    count = cursor.fetchone()[0]
                    print(f"  Rows: {count}")
                except Exception as e:
                    print(f"  Error counting rows: {e}")
            
            conn.close()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            # Print full traceback
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    diagnose_database()