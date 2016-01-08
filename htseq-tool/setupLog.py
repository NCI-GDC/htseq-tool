import errno
import logging

def setup_logging(level, log_name, log_filename):
    """ Sets up a logger """

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    if log_filename == None:
        sh = logging.StreamHandler()
    else:
        sh = logging.FileHandler(log_filename, mode='w')

    sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(sh)
    return logger
