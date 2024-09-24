from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.scheduler import schedule_task, remove_task, scheduler
from app.tasks.example_task import sample_task
from app.utils.auth import create_access_token, verify_token, get_password_hash, verify_password
from app.db.models import SessionLocal, User
from datetime import timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/token")
async def login_for_access_token(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/")
async def register_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(password).decode("utf-8")
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@router.post("/schedule/")
async def schedule(cron_expression: str, task_id: str, username: str = Depends(verify_token)):
    schedule_task(sample_task, cron_expression, task_id)
    return {"message": f"Task {task_id} scheduled"}

@router.delete("/remove/")
async def remove(task_id: str, username: str = Depends(verify_token)):
    remove_task(task_id)
    return {"message": f"Task {task_id} removed"}

@router.get("/status/")
async def task_status(task_id: str, username: str = Depends(verify_token)):
    job = scheduler.get_job(task_id)
    if job:
        return {
            "task_id": task_id,
            "next_run_time": str(job.next_run_time),
            "status": "Scheduled"
        }
    else:
        return {"message": f"Task {task_id} not found"}
