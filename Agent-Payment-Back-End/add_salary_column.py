from app.database import engine
from sqlalchemy import text

def add_salary_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE agents ADD COLUMN salary FLOAT DEFAULT 0.0"))
            print("Successfully added 'salary' column to 'agents' table.")
        except Exception as e:
            print(f"Error (column might already exist): {e}")

if __name__ == "__main__":
    add_salary_column()
