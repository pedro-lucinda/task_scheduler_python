import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.core.scheduler import start_scheduler
from app.utils.logging import setup_logging
from app.api.routes import router
from app.db.models import init_db

load_dotenv()

app = FastAPI()
logger = setup_logging()

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    init_db()  # Initialize the database
    logger.info("Scheduler started and DB initialized")

app.include_router(router)
