import logging


class DefaultPatchedLogger(logging.Logger):
    """
    TODO: Documentation..
    """
    def __init__(self, name) -> None:
        logging.Logger.__init__(self, name)

    def makeRecord(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ) -> logging.LogRecord:
        """
        :param name:
        :param level:
        :param fn:
        :param lno:
        :param msg:
        :param args:
        :param exc_info:
        :param func:
        :param extra:
        :param sinfo:
        :return:
        """
        record = logging.Logger.makeRecord(self, name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

        if extra:
            record.extra = extra.copy()
        
        return record
