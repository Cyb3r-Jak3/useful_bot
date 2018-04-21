# External
import logging
# Internal
import botinfo


def make_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(botinfo.logging_level)
    formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(asctime)s - %(message)s',
        '%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler("bot.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
