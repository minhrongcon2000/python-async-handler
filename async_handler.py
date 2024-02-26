import atexit
from logging import Handler
from logging.config import ConvertingDict, ConvertingList, valid_ident
from logging.handlers import QueueHandler, QueueListener
from queue import Queue, SimpleQueue
from typing import Any, Dict, List, Union

HANDLER_ARG_TYPE = Union[ConvertingList[Dict[str, Any]], List[Handler]]

QUEUE_ARG_TYPE = Union[ConvertingDict[str, Any], Queue[Handler]]


def _resolveChildrenConfig(handlers: HANDLER_ARG_TYPE) -> List[Handler]:
    """Borrow from original logging module!"""
    if not isinstance(handlers, ConvertingList):
        return handlers

    deferred = []
    adj_hdlr = []

    configurator = handlers.configurator

    for hdlr_conf in handlers:
        try:
            handler = configurator.configure_handler(hdlr_conf)
            adj_hdlr.append(handler)
        except Exception as e:
            if "target not configured yet" in str(e.__cause__):
                deferred.append(hdlr_conf)
            else:
                raise

    # Now do any that were deferred
    for hdlr_conf in deferred:
        try:
            handler = configurator.configure_handler(hdlr_conf)
            adj_hdlr.append(handler)
        except Exception as e:
            raise

    return adj_hdlr


def _resolveQueue(q: QUEUE_ARG_TYPE) -> Queue[Handler]:
    """Copy from https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a.
    However, don't follow the handler, it's bugged as of Python >= 3.7 (not sure what Python version this blog is written on)
    """
    if not isinstance(q, ConvertingDict):
        return q

    if "__resolved_value__" in q:
        return q["__resolved_value__"]

    cname = q.pop("class")
    klass = q.configurator.resolve(cname)
    props = q.pop(".", None)
    kwargs = {k: q[k] for k in q if valid_ident(k)}
    result = klass(**kwargs)
    if props:
        for name, value in props.items():
            setattr(result, name, value)

    q["__resolved_value__"] = result
    return result


class AsyncHandler(QueueHandler):
    def __init__(
        self,
        handlers: HANDLER_ARG_TYPE,
        queue: QUEUE_ARG_TYPE = SimpleQueue(),
        respect_handler_level: bool = False,
    ) -> None:
        super().__init__(queue)
        adj_hdlrs = _resolveChildrenConfig(handlers)
        self.queue = _resolveQueue(queue)
        self._worker = QueueListener(
            self.queue, *adj_hdlrs, respect_handler_level=respect_handler_level
        )
        self._worker.start()
        atexit.register(self._worker.stop)
