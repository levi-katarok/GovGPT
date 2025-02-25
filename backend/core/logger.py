import logging


def get_logger(logger_name, log_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False  # Prevent log propagation to avoid double logging

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # Create a FileHandler to write logs to a file

    file_handler = logging.FileHandler("db_timings.log")
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
