from loguru import logger
import asyncio

async def sample_task():
    logger.info("Sample task started.")
    await asyncio.sleep(2)  # Simulate a task that takes some time
    logger.info("Sample task completed.")
