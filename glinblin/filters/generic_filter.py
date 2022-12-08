import logging


class DefaultFilter(logging.Filter):
    """

    """
    def __init__(self, criteria_func=None):
        """

        :param criteria_func: A boolean function criteria to be applied in order to
                         filter the message.
                         The message must follow the format:
                         def criteria_func(message:str = None) -> bool:
                             if your logic here is true:
                                 return True
                             else:
                                 return false
                         Obs 1: Only not None message will be passed, you shouldn't care about it.
                         Obs 2: The criteria function must return Boolean ones, avoiding side-effects.
        """
        if not criteria_func:
            raise ValueError("criteria function must be provided.")
        self.__criteria_func = criteria_func

    def filter(self, record: logging.LogRecord) -> bool:
        """"""
        message = record.getMessage()
        if message:
            return self.__criteria_func(message)
        else:
            return False
