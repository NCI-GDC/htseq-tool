import logging
import gzip

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(name)12s][%(levelname)7s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_open_function(fil):
    if fil.endswith('.gz'):
        return gzip.open
    else:
        return open
