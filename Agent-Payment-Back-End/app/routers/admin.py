from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.deps import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/reset-database", status_code=status.HTTP_204_NO_CONTENT)
def reset_database(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        # Truncate tables and restart identity (reset IDs)
        # RESTART IDENTITY resets the serial counters
        # CASCADE ensures dependent rows are deleted (though we are truncating both)
        db.execute(text("TRUNCATE TABLE payments, agents RESTART IDENTITY CASCADE;"))
        db.commit()
        print("Database reset successfully")
    except Exception as e:
        print(f"Error resetting database: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database reset failed: {str(e)}")
