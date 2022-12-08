import logging
from typing import MutableMapping, Any


class GlinblinFormatter(logging.Formatter):
    """

    """
    def __init__(self, metadata: MutableMapping[str, Any] = None):
        """

        :param extra:
        """
        self.__metadata = dict()
        if metadata:
            self.__metadata = metadata.copy()

        self.fmt = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s - extra: %(extra)s"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        logging.Formatter.__init__(self, fmt=self.fmt, datefmt=self.datefmt)

    @staticmethod
    def has_extra(record: logging.LogRecord) -> bool:
        return hasattr(record, 'extra')

    def format_to_json(self, record: logging.LogRecord) -> MutableMapping[str, Any]:
        """
        :param record:
        :return:
        """
        _ = self.format(record)
        message_output = dict()

        if self.__metadata:
            message_output = self.__metadata.copy()

        message_output["timestamp"] = record.asctime
        message_output["message"] = record.msg

        if GlinblinFormatter.has_extra(record):
            message_output.update(record.extra)

        return message_output

    def format(self, record: logging.LogRecord) -> str:
        if not GlinblinFormatter.has_extra(record):
            record.extra = {}

        return logging.Formatter.format(self, record)


