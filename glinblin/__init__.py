import logging
from typing import MutableMapping, Any, Optional

from .adapters.glinblin_adapter import GlinblinAdapter
from .handlers.elasticsearch_handler import ElasticSearchHandler
from .patched_logger.default_patched_logger import DefaultPatchedLogger
from .formatters.glinblin_formatter import GlinblinFormatter


def get_logger(
        raise_glinblin_exceptions: bool = False,
        logger_name: str = None,
        logger_class: logging.Logger = None,
        logger_formatter: logging.Formatter = None,
        logger_level: int = logging.NOTSET,
        logger_adapter: logging.LoggerAdapter = None,
        logger_handler: logging.Handler = None,
        app_metadata: Optional[MutableMapping[str, Any]] = None) -> logging.Logger:
    """

    :param raise_glinblin_exceptions:
        If true rise internal glinbling exceptions to the caller. Default False will not break the caller workflow.
    :param logger_name: The name of the logger, it must be unique to preserve internal python logging dictionary,
                        otherwise it is going to change an existent one.
    :param logger_class:
        If you have any custom Logger class you can pass it here(not the instance, but the class itself)
    :param logger_formatter:
        An custom formatter instance to be used in logger and handler. The default is GlinblinFormatter
    :param logger_level: The logger level to be used. Sample of values: logging.DEBUG, logging.INFO. Default:
        logging.NOSET
    :param logger_adapter: A custom adapter to change the default Logger's behavior in any aspect.
                           For instance, the GlinblinAdapter modify record in order to put an extra attribute
                           extra, to guard all extra arbitrary fields from .warn, .info, etc, calls. In this way
                           there is no need to iterate over __dict__ to exclude what we do not need to send to the
                           destination handler.
    :param logger_handler: It allows us to pass one handler to be added to logger. If you would like to add another
        handler you can do it outside as well.
    :param app_metadata: A dictionary which holds fixed information which will appears alongside every log message.
        As an useful sample, we could have the following format:
        {
           "app_id": <a unique identifier of the application>,
           "app_name": <the name of the application invoking logger>,
           "cloud_account_id": <the owner of the account in question. Depending on the
           cloud(AWS, Azure, Google Cloud Platform) where your application is
            running it could assume different value formats.
    :return:
    """
    logging.raiseExceptions = raise_glinblin_exceptions

    if not logger_class:
        logging.setLoggerClass(DefaultPatchedLogger)
    else:
        logging.setLoggerClass(logger_class)

    # We have to setting up logger instance, only after setting LoggerClass
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    if not app_metadata:
        app_metadata = dict()

    formatter = GlinblinFormatter(metadata=app_metadata) if not logger_formatter else logger_formatter
    adapter = GlinblinAdapter(logger=logger, metadata=app_metadata) if not logger_adapter else logger_adapter
    handler = ElasticSearchHandler(logger_level=logger_level, fmt=formatter) if not logger_handler else logger_handler

    # stdout
    logging.basicConfig(format=formatter.fmt)

    logger.addHandler(handler)
    logger = adapter

    return logger
