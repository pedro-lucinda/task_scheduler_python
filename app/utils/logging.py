from loguru import logger

def setup_logging():
    logger.add("logs/scheduler.log", rotation="1 MB", level="INFO")
    return logger
