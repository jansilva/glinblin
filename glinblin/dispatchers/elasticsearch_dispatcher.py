import threading
import multiprocessing

from queue import Queue
from typing import Dict

from glinblin.utils.custom_types import JSONType


class DispatcherWorker(threading.Thread):

    def __init__(self, queue: Queue):
        threading.Thread.__init__(self, name="dispatcher-worker", daemon=True)
        self.__queue = queue
        self.__stop = threading.Event()

    def consume_queue(self):
        try:
            message = self.__queue.get()
            print(
                f"[{multiprocessing.current_process().name}]\
                [{threading.current_thread().name}] [{threading.current_thread().native_id}] \
                - send_message, with message: {message}"
            )
        finally:
            self.__queue.task_done()

    def run(self):
        while not self.__stop.is_set():
            self.consume_queue()

    def flush(self):
        print(f"entering flush queue size: {self.__queue.qsize()}")
        while not self.__queue.empty():
            print(f"Sending remaining messages...")
            self.consume_queue()
        print(f"exiting flush queue size: {self.__queue.qsize()}")

    def join(self, timeout=5):
        """ Stop the thread. """
        self.__stop.set()
        self.flush()
        threading.Thread.join(self, timeout=timeout)


class ElasticSearchDispatcher:
    """
    A singleton thread-safe class that holds
    message queue and dispatching it to the right destination.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ElasticSearchDispatcher, cls).__new__(cls)
        return cls.instance

    def __init__(self, max_buffer_size: int = 10000, **elasticsearch_config: Dict):
        """

        :param config: The ElasticSearch configuration setup.
        """
        self.__message_queue = Queue(maxsize=max_buffer_size)
        # The consumer thread to use aiohttp in order to send message
        # to ElasticSearch.
        self.__dispatcher = DispatcherWorker(self.__message_queue)
        self.__dispatcher.start()

    def enqueue_message(self, message: JSONType) -> None:
        """
        In case of failure while trying to enqueue message, this module
        shouldn't propagate error to the caller, just log message normally.
        Unless the flag throw_error_while_enqueue was configured with True value.
        :param message: A JSON object to send to the destination.
        :return: None
        """
        # print(f"Putting {message} into queue.")
        self.__message_queue.put(message)

    def finish_dispatcher(self):
        """
        Finishes the consumer thread.
        :return:
        """
        self.__dispatcher.join()
