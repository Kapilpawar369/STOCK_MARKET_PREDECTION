import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")


# Custom Log Formatter
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)


#Create main logger instance
logger = logging.getLogger("stockpulse")
logger.setLevel(logging.DEBUG)   # DEBUG → Dev | INFO → Prod


# Console Handler (Terminal Logs)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)


# App File Handler (Rotates Daily)
file_handler = TimedRotatingFileHandler(
    APP_LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=15,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)


# Error File Handler (Separate ERROR logs)
error_file_handler = TimedRotatingFileHandler(
    ERROR_LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)


# Avoid duplicate logs
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)


#Production Safety
logger.propagate = False
