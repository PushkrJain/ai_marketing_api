import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_research_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "research.log")

    logger = logging.getLogger("research_logger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # --- LOG ROTATION ENABLED ---
        fh = TimedRotatingFileHandler(
            log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8'
        )
        # --- TO DISABLE LOG ROTATION ---
        # from logging import FileHandler
        # fh = FileHandler(log_file, mode='a', encoding='utf-8')

        formatter = logging.Formatter('%(asctime)s - INFO - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

research_logger = setup_research_logger()

