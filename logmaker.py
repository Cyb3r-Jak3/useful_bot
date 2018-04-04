import logging


def makeLogger(Name):
    loggerName = Name
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    logFile = "bot.log"
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh = logging.FileHandler(logFile)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
