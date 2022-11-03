import logging
from typing import Mapping


class GlinblinLog:
    def __init__(self):
        pass

    def setup_from_file(self, config_file_path=None) -> Mapping:
        pass

    def setup_from_arguments(self) -> Mapping:
        pass

    def __format(self) -> str:
        pass

    def __enqueue_message(self) -> bool:
        pass

    def send(self) -> None:
        pass

    def info(self, message:str=None) -> None:
        pass

    def info(self, message:str=None) -> None:
        pass

    def debug(self, message:str=None) -> None:
        pass

    def warning(self, message:str=None) -> None:
        pass

    def error(self, message:str=None) -> None:
        pass

    def critical(self, message:str=None) -> None:
        pass

    def not_set(self, message:str=None) -> None:
        pass