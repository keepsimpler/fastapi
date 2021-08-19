from app.db.session import SessionLocal

def test_db_session():
    db = SessionLocal()
    db.execute("SELECT 1")
    return