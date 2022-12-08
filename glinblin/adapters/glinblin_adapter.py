import logging
from typing import MutableMapping, Any


class GlinblinAdapter(logging.LoggerAdapter):
    """

    """
    def __init__(
            self,
            logger: logging.Logger = None,
            metadata: MutableMapping[str, Any] = None):
        """
        :param metadata: A dictionary with the following entries:
                      application_name: <the name of the application>,
                      cloud_account_id:
                          <the identifier of the cloud account owner for google/azure/aws>
                      <other entries>

        """
        extra = dict()

        if metadata:
            extra.update(metadata)

        logging.LoggerAdapter.__init__(self, logger=logger, extra=extra)

    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> tuple[Any, MutableMapping[str, Any]]:
        context_info = kwargs.get("extra")

        if context_info:
            self.extra.update(context_info)

        return logging.LoggerAdapter.process(self, msg, kwargs)
