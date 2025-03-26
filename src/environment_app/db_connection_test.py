import sqlite3
import os

# Path to the database
DB_PATH = "/Users/linakalai/Desktop/UCL/PersonalApp/src/environment_app/instance/environment.db"

def test_sqlite_connection():
    """Test direct SQLite connection"""
    try:
        # Attempt to connect to the database
        conn = sqlite3.connect(DB_PATH)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Successfully connected to the database!")
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
            
            # Count rows in each table
            cursor.execute(f"SELECT COUNT(*) FROM '{table[0]}'")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
        
        # Close the connection
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    try:
        # Create an engine
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test a simple query
        from environment_app.flask_app.models import Borough
        boroughs = session.query(Borough).all()
        
        print("\nSQLAlchemy connection successful!")
        print(f"Number of boroughs: {len(boroughs)}")
        
        # Close the session
        session.close()
        
    except Exception as e:
        print(f"SQLAlchemy connection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing SQLite direct connection:")
    test_sqlite_connection()
    
    print("\n" + "="*40 + "\n")
    
    print("Testing SQLAlchemy connection:")
    test_sqlalchemy_connection()