import logging
from typing import Union
import threading
import multiprocessing

from ..dispatchers.elasticsearch_dispatcher import ElasticSearchDispatcher
from ..formatters.default_formatter import DEFAULT_FMT_STR, DEFAULT_FMT_DATETIME


class ElasticSearchHandler(logging.Handler):
    """
    This handler sends log records to an Elasticsearch
    destination, according to provided configuration.
    """
    def __init__(
            self,
            application_name: str = None,
            level: Union[int, str] = logging.DEBUG,
            fmt: logging.Formatter = None
        ):
        logging.Handler.__init__(self, level)
        self.__fmt = fmt
        if not self.__fmt:
            self.__fmt = logging.Formatter(fmt=DEFAULT_FMT_STR, datefmt=DEFAULT_FMT_DATETIME)

        super(ElasticSearchHandler, self).setFormatter(self.__fmt)

        self.__dispatcher = ElasticSearchDispatcher()

    def emit(self, record: logging.LogRecord) -> None:
        """
        when a message is produced emit is triggered in order
        to dispatch the message.
        The message will be stored into a thread-safe queue(a FIFO buffer),
        after it a separated thread(dispatcher) will send it asynchronously to the
        destination.
        :param record: A logger message
        :return: None
        """
        print(f"record: {record.__dict__}")
        message = self.format(record)
        self.__dispatcher.enqueue_message(message)

    def close(self):
        self.__dispatcher.finish_dispatcher()
