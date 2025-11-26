from logging.config import dictConfig

def setup_logging():
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "uvicorn": {
                 "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(levelname)-8s%(reset)s- %(asctime)s | %(name)s | %(funcName)s() - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "uvicorn",
                "level": "DEBUG",
            },
        },

        "loggers": {
            # Your app logger
            "app": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },

            # Keep uvicorn logs untouched
            "uvicorn.error": {
                "level": "INFO",
                "propagate": True
            },
            "uvicorn.access": {
                "level": "INFO",
                "propagate": True
            }
        }
    })