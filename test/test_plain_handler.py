import logging
import logging.config
import time
import unittest
from io import StringIO

from async_handler import AsyncHandler


class BasicUsageTest(unittest.TestCase):

    def testPlainUsage(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        mockLogStream = StringIO()

        hdlr = AsyncHandler(
            [
                logging.FileHandler("app.log", mode="w"),
                logging.StreamHandler(stream=mockLogStream),
            ]
        )
        logger.addHandler(hdlr)
        logger.info("hello")

        time.sleep(1)

        mockLogStream.seek(0)
        self.assertEqual(mockLogStream.read(), "hello\n")

        with open("app.log") as f:
            self.assertEqual(f.read(), "hello\n")

    def testConfigUsage(self):
        mockLogStream = StringIO()
        LOGGING = {
            "version": 1,
            "handlers": {
                "qhandler": {
                    "class": "async_handler.AsyncHandler",
                    "queue": {
                        "class": "queue.Queue",
                    },
                    "handlers": [
                        {
                            "class": "logging.StreamHandler",
                            "stream": mockLogStream,
                        },
                        {
                            "class": "logging.FileHandler",
                            "filename": "app.log",
                            "mode": "w",
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

        time.sleep(1)

        mockLogStream.seek(0)
        self.assertEqual(mockLogStream.read(), "hello\n")
        print(mockLogStream.read())

        with open("app.log") as f:
            self.assertEqual(f.read(), "hello\n")
