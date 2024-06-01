import logging
from typing import Any, Dict

from pythonjsonlogger import jsonlogger

DEFAULT_LOG_LEVEL: int = logging.INFO
DEFAULT_LOG_FORMAT: str = '%(levelname)s %(asctime)s %(module)s %(message)s'


class AzureJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, fmt: str = DEFAULT_LOG_FORMAT, style: str = '%', *args: Any, **kwargs: Any) -> None:
        super().__init__(fmt=fmt, *args, **kwargs)

    def process_log_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        log_dict: Dict[str, Any] = dict(record)

        log_dict['severity'] = log_dict['levelname']
        log_dict['logger'] = log_dict.get('name')

        if 'exc_info' in log_dict:
            log_dict['exc_info'] = str(log_dict['exc_info'])

        return super().process_log_record(log_dict)


def configure_logging() -> logging.Logger:
    default_logger = logging.getLogger(__name__)
    default_logger.setLevel(DEFAULT_LOG_LEVEL)
    default_logger.handlers = []

    # Create a stream handler that outputs to sys.stderr
    stream_logger = logging.StreamHandler()
    stream_logger.setLevel(DEFAULT_LOG_LEVEL)
    stream_logger.setFormatter(AzureJsonFormatter())
    default_logger.addHandler(stream_logger)
    return default_logger
