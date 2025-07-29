from labgenpackage.classes import CustomFormatter
from gui.app_frame import App

import logging, logging.config

#Logger setup
def setup_logger() -> logging.Logger:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "{levelname} - {name}: {message}",
                "style":"{"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                #"formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "debug_rotating_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "mode": "a",
                "filename": "debug.log",
                "maxBytes": 150000,
                "backupCount": 3,
                "encoding":"utf-8"
            }
        },
        "loggers": {
            "root": {"level": "INFO", "handlers": ["stdout", "debug_rotating_file_handler"]}
        }
    }
    logging.config.dictConfig(config=logging_config)
    ch = logging.getHandlerByName("stdout")
    ch1 = logging.getHandlerByName("debug_rotating_file_handler")
    ch.setFormatter(CustomFormatter())
    ch1.setFormatter(CustomFormatter())
    logger = logging.getLogger("my_app")
    return logger

#main function
def main():
    try:
        #init logger
        logger = setup_logger()

        #init main app widget
        app = App()

        #init main loop
        app.mainloop()

    except Exception as e:
        logger.exception(f"Error: {e}. Exiting app!")
        exit()

if __name__ == "__main__":
    main()