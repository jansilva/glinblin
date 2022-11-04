import logging
from typing import Mapping
from enum import Enum, auto


class Severity(Enum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    NOT_SET = auto()


class Logger:

    def __init__(self):
        pass

    def setup_from_file(self, config_file_path: str) -> Mapping:
        pass

    def setup_from_arguments(self) -> Mapping:
        pass

    def __format(self) -> str:
        pass

    def __enqueue_message(self) -> bool:
        pass

    def log(self, severity: Severity, message: str) -> None:
        # print(f"Your package is running...")
        pass

