import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            #"module": record.module,
            #"function": record.funcName,
            #"line": record.lineno
        }
        return json.dumps(log_record)

def setup_logger(log_file: str, 
                 log_level: int = logging.INFO,
                 logger_name: str = 'default',
                 max_size: int = 1_000_000,
                 backups: int = 3):
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Create a rotating file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000, 
        backupCount=backups  
    )
    file_handler.setLevel(log_level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatters
    formatter = JsonFormatter()
    standard_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a formatter
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
