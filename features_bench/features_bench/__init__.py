import logging
import re
import sys
from collections import OrderedDict

import structlog


class StripAnsiFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def filter(self, record):
        if hasattr(record, "msg"):
            record.msg = self.ansi_escape.sub("", str(record.msg))
        return True


# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

# Add file handler with ANSI filter
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(message)s"))
file_handler.addFilter(StripAnsiFilter())  # Add the filter here
logging.getLogger().addHandler(file_handler)

# Keep your existing structlog configuration with colors
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
        structlog.dev.ConsoleRenderer(
            colors=True, force_colors=True, repr_native_str=False, pad_event=25
        ),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=OrderedDict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
