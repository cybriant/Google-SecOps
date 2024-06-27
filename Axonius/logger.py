import logging

def main():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    myLogger = logging.getLogger(__name__)
    myLogger.setLevel('DEBUG')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(formatter)
    myLogger.addHandler(stream_handler)
    return myLogger
