import logging
import tempfile
import time

import pytest

from async_handler import AsyncHandler


@pytest.fixture
def logFile():
    tmpfile = tempfile.NamedTemporaryFile()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    hdlr = AsyncHandler(
        [
            logging.StreamHandler(),
            logging.FileHandler(tmpfile.name),
        ]
    )
    logger.addHandler(hdlr)
    logger.info("hello")
    time.sleep(2)
    logging.shutdown()

    yield tmpfile
    tmpfile.close()


def testPlainUsage(caplog, logFile):
    for record in caplog.records:
        assert record.message == "hello"
        assert record.levelno == logging.INFO

    assert logFile.read().decode() == "hello\n"
