import threading
import multiprocessing

from queue import Queue


class DispatcherWorker(threading.Thread):

    def __init__(self, buffer: Queue = None):
        threading.Thread.__init__(self, daemon=True)
        self.__buffer = buffer
        self.__stop = threading.Event()

    def consume_buffer(self):
        try:
            message = self.__buffer.get()
            print(
                f"[{multiprocessing.current_process().name}]\
                [{threading.current_thread().name}] [{threading.current_thread().native_id}] \
                - send_message, with message: {message}"
            )
        finally:
            self.__buffer.task_done()

    def run(self):
        while not self.__stop.is_set():
            self.consume_buffer()

    def flush(self):
        while not self.__buffer.empty():
            self.consume_buffer()

    def join(self, timeout=3):
        """ It stops the thread. """
        self.__stop.set()
        self.flush()
        threading.Thread.join(self, timeout=timeout)
