from typing import Any, Dict

dict_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(asctime)s | %(filename)s |"
            " %(funcName)s | %(levelname)s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
        },
    },
    "loggers": {
        "main": {"level": "DEBUG", "handlers": ["console"], "propagate": False}
    },
}
