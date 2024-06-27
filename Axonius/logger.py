import logging

def main(logDest):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    myLogger = logging.getLogger(__name__)
    myLogger.setLevel('DEBUG')
    file_handler = logging.FileHandler(logDest)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    myLogger.addHandler(file_handler)
    return myLogger
