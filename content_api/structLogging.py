import logging, sys, structlog
from datetime import datetime, timezone
from flask import g
from uuid import uuid4




def add_timestamp(_, __, event_dict):
    event_dict["timestamp"] = datetime.now(timezone.utc).isoformat()
    return event_dict
def add_correlation_id(_, __, event_dict):
    event_dict["correlation_id"] = getattr(g, "correlation_id", None)
    return event_dict



wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG)

def configure_logging():
    """
    Configure structlog with JSON output, timestamps, and log levels.
    Integrates with Python's standard logging.
    """
    logging.basicConfig(
        stream=sys.stdout, 
        format="%(message)s",
        level=logging.DEBUG)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),  # Add ISO timestamp
            structlog.stdlib.add_log_level,               # Include log level
            add_timestamp,
            add_correlation_id,
            structlog.processors.StackInfoRenderer(),     # Optional: stack info
            structlog.processors.format_exc_info,         # Exception formatting
            structlog.processors.JSONRenderer()           # Output logs as JSON
        ],
        context_class=dict,                               # Store context in dict
        logger_factory=structlog.stdlib.LoggerFactory(),  # Use stdlib logger
        wrapper_class=structlog.stdlib.BoundLogger,       # Bound logger
        cache_logger_on_first_use=True
    )
    log = structlog.get_logger()
    return log

