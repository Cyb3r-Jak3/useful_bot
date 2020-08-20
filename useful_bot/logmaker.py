"""Makes the log files"""
# External
import logging

# Internal
import botinfo


def make_logger(name: str) -> logging.Logger:
    """
    Creates the logger class. Used in a lot of my programs
    Parameters
    ----------
    name: str
        name of the logger to create

    Returns
    -------
        The logger class
    """
    logger = logging.getLogger(name)
    logger.setLevel(botinfo.logging_level)
    formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler("bot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
