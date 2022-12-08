import logging

from glinblin import get_logger


if __name__ == "__main__":
    logger = get_logger(
        raise_glinblin_exceptions=True,
        logger_name="test_jan",
        logger_level=logging.DEBUG,
        app_metadata={
            "app_id": "a12f5627-a0f9-4fea-bc75-cb0ccd2476f4",
            "app_name": __name__,
            "cloud_account_id": "33344445563-1"
        }
    )
    logger.debug("xpto", extra={"start": "init", "test": 445})
