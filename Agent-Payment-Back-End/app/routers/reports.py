from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.database import SessionLocal
from app.models import Payment
from fastapi.responses import FileResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/payments/pdf")
def payments_pdf():
    file = "payments.pdf"
    c = canvas.Canvas(file, pagesize=A4)
    y = 800

    c.drawString(200, y, "Payments Report")
    y -= 40

    db = SessionLocal()
    payments = db.query(Payment).all()

    for p in payments:
        c.drawString(50, y, f"Agent ID: {p.agent_id} | Amount: {p.amount} | {p.status}")
        y -= 20

    c.save()
    return FileResponse(file, filename="payments.pdf")

# ✅ NEW: Dashboard Stats Endpoint
from sqlalchemy import func
from app.models import Agent

from typing import Optional
from datetime import date, datetime, timedelta

@router.get("/dashboard")
def get_dashboard_stats(month: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        # Base Query
        query = db.query(Payment)

        # Apply Month Filter
        if month:
            # Expected format: YYYY-MM
            try:
                start_date = datetime.strptime(month, "%Y-%m").date()
                # Calculate end of month
                if start_date.month == 12:
                    end_date = date(start_date.year + 1, 1, 1)
                else:
                    end_date = date(start_date.year, start_date.month + 1, 1)
                
                query = query.filter(Payment.payment_date >= start_date, Payment.payment_date < end_date)
            except ValueError:
                pass # Invalid date format, ignore filter

        # Total Agents (Always global)
        total_agents = db.query(Agent).count()

        # Monthly Payments (Sum of filtered payments)
        monthly_payments = query.with_entities(func.sum(Payment.amount)).scalar() or 0.0

        # Status Counts (Filtered)
        pending_count = query.filter(func.lower(Payment.status) == "pending").count()
        completed_count = query.filter(func.lower(Payment.status) == "completed").count()
        failed_count = query.filter(func.lower(Payment.status) == "failed").count()
        cancelled_count = query.filter(func.lower(Payment.status) == "cancelled").count()

        # Recent Payments (Filtered)
        recent_payments = query.order_by(Payment.id.desc()).limit(5).all()

        return {
            "total_agents": total_agents,
            "monthly_payments": monthly_payments,
            "pending_count": pending_count,
            "completed_count": completed_count,
            "failed_count": failed_count,
            "cancelled_count": cancelled_count,
            "recent_payments": recent_payments
        }
    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        return {
            "total_agents": 0,
            "monthly_payments": 0,
            "pending_count": 0,
            "completed_count": 0,
            "failed_count": 0,
            "cancelled_count": 0,
            "recent_payments": []
        }
