# logger_setup.py
import logging
import os
# --- Import the helper function from our database script ---
from database import get_base_path

# --- Use the helper function to define the logs directory path ---
LOGS_DIR = os.path.join(get_base_path(), 'logs')

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

loggers = {}

def get_logger_for_ip(ip_address):
    """Creates or gets a unique logger for a specific IP address."""
    global loggers

    if loggers.get(ip_address):
        return loggers.get(ip_address)
    else:
        logger = logging.getLogger(ip_address)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        
        # Use the full path for the log file
        log_file_path = os.path.join(LOGS_DIR, f'{ip_address}.log')
        handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
        
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        
        if not logger.handlers:
            logger.addHandler(handler)
            
        loggers[ip_address] = logger
        return logger