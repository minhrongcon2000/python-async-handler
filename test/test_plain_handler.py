import logging
import logging.config
import os
import tempfile
import time
import unittest
from io import StringIO

from async_handler import AsyncHandler


class BasicUsageTest(unittest.TestCase):

    def testPlainUsage(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        hdlr = AsyncHandler([logging.StreamHandler(), logging.FileHandler("app.log")])
        logger.addHandler(hdlr)
        logger.info("hello")

    def testConfigUsage(self):
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
                            "filename": "app.log",
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
