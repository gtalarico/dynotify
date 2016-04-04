import os

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

LOGGER_CONFIG = {
  "version": 1,
  "disable_existing_loggers": True,
  "handlers":
  {
      "console": {
          "class": "logging.StreamHandler",
          "formatter": "simple"
              },

      "file_latest": {
         "class": "logging.FileHandler",
          "level": "DEBUG",
          "formatter": "simple",
          "filename": os.path.join(LOG_PATH,"log_latest.log"),
          "mode": "w"
              },

      "info_file_handler": {
          "class": "logging.handlers.RotatingFileHandler",
          "level": "INFO",
          "formatter": "simple",
          "filename": os.path.join(LOG_PATH,"info.log"),
          "maxBytes": 10485760,
          "backupCount": 20,
          "encoding": "utf8"
                          },

      "error_file_handler": {
          "class": "logging.handlers.RotatingFileHandler",
          "level": "ERROR",
          "formatter": "complete",
          "filename": os.path.join(LOG_PATH,"errors.log"),
          "maxBytes": 10485760,
          "backupCount": 20,
          "encoding": "utf8"
                          }
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
                  "handlers": ["console", "file_latest","info_file_handler","error_file_handler"],
                  "level": os.getenv('DJANGO_LOG_LEVEL', 'INFO')
              },
         }
  }
