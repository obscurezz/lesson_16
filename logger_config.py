import logging

FORMAT = '%(asctime)s [%(levelname)s] %(message)s'


def get_file_handler(log_name):
    file_handler = logging.FileHandler(log_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(FORMAT))
    return stream_handler


def get_logger(name, log_name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler(log_name))
    logger.addHandler(get_stream_handler())
    return logger
