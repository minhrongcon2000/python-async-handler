import logging
import logging.config
import tempfile
import time

import pytest


@pytest.fixture
def logFile():
    tmpfile = tempfile.NamedTemporaryFile()
    LOGGING = {
        "version": 1,
        "handlers": {
            "qhandler": {
                "class": "async_handler.AsyncHandler",
                "handlers": [
                    {
                        "class": "logging.StreamHandler",
                    },
                    {
                        "class": "logging.FileHandler",
                        "filename": tmpfile.name,
                    },
                ],
            },
        },
        "loggers": {
            "root": {
                "handlers": ["qhandler"],
                "level": "INFO",
            },
        },
    }
    logging.config.dictConfig(LOGGING)

    logger = logging.getLogger(__name__)

    logger.info("hello")
    time.sleep(2)
    logging.shutdown()

    yield tmpfile

    tmpfile.close()


def testConfigUsage(caplog, logFile):
    for record in caplog.records:
        assert record.message == "hello"
        assert record.levelno == logging.INFO

    assert logFile.read().decode() == "hello\n"
