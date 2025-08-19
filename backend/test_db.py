from sqlalchemy import text
from app.db import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))  # ✅ wrap in text()
            print("✅ Connection successful:", result.scalar())
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection()
