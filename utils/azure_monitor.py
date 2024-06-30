import logging

from pythonjsonlogger import jsonlogger

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(levelname)s %(asctime)s %(module)s %(message)s'


class AzureJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, fmt=DEFAULT_LOG_FORMAT, style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, record):
        log_dict = dict(record)

        log_dict['severity'] = log_dict['levelname']
        log_dict['logger'] = log_dict.get('name')

        if 'exc_info' in log_dict:
            log_dict['exc_info'] = str(log_dict['exc_info'])

        return super(AzureJsonFormatter, self).process_log_record(log_dict)


def configure_logging():
    # Get the root logger
    default_logger = logging.getLogger()
    default_logger.setLevel(DEFAULT_LOG_LEVEL)
    default_logger.handlers = []

    # Create a stream handler that outputs to sys.stderr
    stream_logger = logging.StreamHandler()
    stream_logger.setLevel(DEFAULT_LOG_LEVEL)
    stream_logger.setFormatter(AzureJsonFormatter())
    default_logger.addHandler(stream_logger)
