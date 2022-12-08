import logging
import time

from typing import Union, Dict, MutableMapping, Any
from queue import Queue

from ..dispatchers.http_async_dispatcher import DispatcherWorker


class ElasticSearchHandler(logging.Handler):
    """
    This handler sends log records to an Elasticsearch
    destination, according to provided configuration.
    """
    def __init__(
            self,
            logger_level: int = logging.NOTSET,
            fmt: logging.Formatter = None,
            buffer_size: int = 10000):
        """
        This initializes the instance attributes.
        :param logger_level: Log level
                            <logging.INFO|
                             logging.DEBUG|
                             logging.WARNING|
                             logging.ERROR|
                             logging.CRITICAL>
        :param fmt: a formatter to transform the message text.
        :param buffer_size: The size limit of the buffer.
        :param raise_exceptions: If True throw error breaking the caller. Otherwise,
                               Just ignore the error.
        """
        logging.Handler.__init__(self, level=logger_level)
        self.__fmt = fmt
        logging.Handler.setFormatter(self, self.__fmt)

        self.__buffer = Queue(maxsize=buffer_size)
        self.__dispatcher = DispatcherWorker(buffer=self.__buffer)
        self.__dispatcher.start()

    def __add_payload_to_buffer(self, message: MutableMapping[str, Any]) -> None:
        """
        In case of failure while trying to enqueue message, this module
        shouldn't propagate error to the caller, just log message normally.
        Unless the flag throw_error_while_enqueue was configured with True value.
        :param message: A JSON object to send to the destination.
        :return: None
        """
        if self.__dispatcher.is_alive():
            self.__buffer.put(message)

    def emit(self, record: logging.LogRecord) -> None:
        """
        when a message is produced emit is triggered in order
        to dispatch the message.
        The message will be stored into a thread-safe queue(a FIFO buffer),
        after it, a separated thread(dispatcher) will send it asynchronously to the
        destination.
        :param record: A logger JSON structured message
        :return: None
        """
        try:
            payload = self.__fmt.format_to_json(record)
            self.__add_payload_to_buffer(payload)
        except Exception as e:
            logging.Handler.handleError(self, record)

    def close(self):
        """
        Finishes the consumer thread.
        :return:
        """
        self.__dispatcher.join()
