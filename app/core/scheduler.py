from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
from sqlalchemy.orm import Session
from app.db.models import Task, SessionLocal

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_listener(task_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

def schedule_task(func, cron_expression: str, task_id: str):
    # Schedule the task using a cron expression
    trigger = CronTrigger.from_crontab(cron_expression)
    scheduler.add_job(func, trigger, id=task_id, replace_existing=True)
    logging.info(f"Task {task_id} scheduled with cron expression {cron_expression}")
    
    # Save task to the database
    db = SessionLocal()
    task = Task(task_id=task_id, cron_expression=cron_expression)
    db.add(task)
    db.commit()
    db.close()

def remove_task(task_id: str):
    try:
        # First, remove the task from the scheduler
        scheduler.remove_job(task_id)
        logging.info(f"Task {task_id} removed from scheduler")
    except Exception as e:
        logging.error(f"Failed to remove task {task_id} from scheduler: {e}")

    # Remove the task from the database
    db = SessionLocal()
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        logging.info(f"Task {task_id} removed from database")

def task_listener(event):
    if event.exception:
        logging.error(f"Task {event.job_id} failed with error: {event.exception}")
    else:
        logging.info(f"Task {event.job_id} completed successfully")
