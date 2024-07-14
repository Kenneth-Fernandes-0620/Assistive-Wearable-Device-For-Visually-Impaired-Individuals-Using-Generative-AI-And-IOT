import time
import logging


# TODO: Add Documentation
def measure_time(func, *args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return result, elapsed_time


# TODO: Add Documentation
def load_logger(name: str, log_file: str = "logger.log", level: int = logging.INFO) -> logging.Logger:
    """Function to setup a logger with specified name, log file, and logging level."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(level)
        logger.addHandler(handler)

    return logger
