import logging


def configure_logging():
    default_log_level = logging.INFO
    default_log_format = '%(levelname)s %(asctime)s %(module)s %(message)s'

    # Get the root logger
    default_logger = logging.getLogger(__name__)
    default_logger.setLevel(default_log_level)

    # Create a stream handler that outputs to sys.stderr
    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(logging.Formatter(default_log_format))
    default_logger.addHandler(stream_logger)

    return default_logger
