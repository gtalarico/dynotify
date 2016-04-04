import os
import sys

LOGGER_CONFIG = {
    'version': 1,
    "disable_existing_loggers": Fase,
    'handlers': {
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        },
    },
    "formatters": {
        "simple": {
            "format": "[%(levelname)s] %(message)s [%(filename)s](%(lineno)d)",
            "datefmt" : "%I:%M:%S"
            },
        "complete": {
            "format": "%(asctime)s [%(filename)s] - %(levelname)s - %(message)s: Line %(lineno)d [logger: %(name)s / modeule:%(module)s]",
            "datefmt" : "%Y/%m/%d %I:%M:%S %p"
                    }
    },
    "loggers": {
            "": {
                    "handlers": ["console"],
                    "level": os.getenv('DJANGO_LOG_LEVEL', 'ERROR')
            },
       }
}
