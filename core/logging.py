import json
import logging
import sys
from functools import lru_cache


class StructuredFormatter(logging.Formatter):
    """Render standard fields plus any structured `extra={...}` context as JSON."""

    RESERVED = {
        "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
        "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "message", "asctime", "taskName",
    }

    def format(self, record: logging.LogRecord) -> str:
        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k not in self.RESERVED and not k.startswith("_")
        }
        base = super().format(record)
        if extras:
            base += " " + json.dumps(extras, sort_keys=True, default=str)
        return base


def _setup(level: str = "INFO") -> logging.Logger:
    root = logging.getLogger("caira")
    if root.handlers:
        return root

    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        StructuredFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(handler)
    root.propagate = False
    return root


@lru_cache(maxsize=1)
def get_logger(name: str) -> logging.Logger:
    _setup()
    return logging.getLogger(name)
