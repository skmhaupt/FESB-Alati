import argparse
import logging
import logging.config
from labgenpackage.lab_generator_main import main
from labgenpackage.classes import CustomFormatter

#Logger setup
grey = "\\x1b[38;21m"
yellow = "\\x1b[33;21m"
red = "\\x1b[31;21m"
bold_red = "\\x1b[31;1m"
reset = "\\x1b[0m"

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # "formatters": {
    #     "simple": {
    #         "format": "{levelname} - {name}: {message}",
    #         "style":"{"
    #     }
    # },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            #"formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["stdout"]}
    }
}

logging.config.dictConfig(config=logging_config)
ch = logging.getHandlerByName("stdout")
ch.setFormatter(CustomFormatter())
logger = logging.getLogger("my_app")

#argparse setup
cli_parser = argparse.ArgumentParser(description='Create schedule for lab groups.')
cli_parser.add_argument("scraper_state", help="Enable or disable schedule scraper. Allowed inputs are: \"on\" and \"off\".")

args = cli_parser.parse_args()

if args.scraper_state == "off":
    scraper_state = False
elif args.scraper_state == "on":
    scraper_state = True

try:
    main(scraper_state)
except:
    #logging.exception("Error")
    logger.error("Exiting script!")
    exit()

