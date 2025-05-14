import logging
import os
from logging.handlers import TimedRotatingFileHandler

def setup_error_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "error.log")

    logger = logging.getLogger("error_logger")
    logger.setLevel(logging.ERROR)
    # Prevent duplicate handlers
    if not logger.handlers:
        # --- LOG ROTATION ENABLED ---
        # This handler rotates the log at midnight every day and keeps 7 days of logs.
        fh = TimedRotatingFileHandler(
            log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8'
        )
        # --- TO DISABLE LOG ROTATION ---
        # If you do NOT want log rotation and just want a single growing log file,
        # comment out the above handler and uncomment the next two lines:
        # from logging import FileHandler
        # fh = FileHandler(log_file, mode='a', encoding='utf-8')
        
        formatter = logging.Formatter('%(asctime)s - ERROR - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

error_logger = setup_error_logger()

