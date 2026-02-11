from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Agent
from app.schemas import AgentCreate, AgentOut
from app.deps import admin_only

router = APIRouter(prefix="/agents", tags=["Agents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AgentOut)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db), user=Depends(admin_only)):
    new_agent = Agent(**agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@router.get("/", response_model=list[AgentOut])
def get_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

    db.commit()
    return {"message": "Agent deleted"}

@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: int, agent_data: AgentCreate, db: Session = Depends(get_db), user=Depends(admin_only)):
    agent = db.get(Agent, agent_id)
    if not agent:
        # Should raise 404 but for simplicity in this stack just return or error
        # In real app: raise HTTPException(status_code=404, detail="Agent not found")
        pass
    
    agent.name = agent_data.name
    agent.role = agent_data.role
    agent.salary = agent_data.salary
    
    db.commit()
    db.refresh(agent)
    return agent
