import argparse
import logging
import logging.config
from labgenpackage.lab_generator_main import main
from labgenpackage.classes import CustomFormatter

#Logger setup
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
cli_parser.add_argument("-st","--scraper_state", type=str, required=True, choices=["on","off"], default="off",
                        help="Enable or disable schedule scraper. Allowed inputs are: \"on\" and \"off\".")
cli_parser.add_argument("-m", "--mode", type=str, required=True, choices=["mode0","mode1", "mode2"], default="mode0",
                        help="Set method to be used for filling out groups. Allowed inputs are: \"mode0\", \"mode1\" and \"mode2\". Mode0: use standard group filling algorithm that ignores alfabetical priority. Mode1: use the variable group filling algorithm. Mode2: use forced alfabetical algorithm.")
cli_parser.add_argument("-alp", "--alf_prio_lvl", type=int, choices=range(0,101), metavar="[0-100]", default=0,
                        help="Set priority level for alfabetical sorting. Allowed inputs are in range of \"0\" to \"100\". 0: ignore alfabetical order, 100: force alfabetical order.")
cli_parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
args = cli_parser.parse_args()
scraper_state: bool = False
mode: int = 0

if args.verbose:
    logger.setLevel("INFO")
else:
    logger.setLevel("WARNING")

if args.scraper_state == "off":
    scraper_state = False
elif args.scraper_state == "on":
    scraper_state = True

if args.mode == "mode0":
    mode = 0
elif args.mode == "mode1":
    mode = 1
elif args.mode == "mode2":
    logger.warning("Work in progress. Mode2 is not functional.")
    exit()
    mode = 2

try:
    main(scraper_state, mode, args.alf_prio_lvl)
except:
    #logging.exception("Error")
    logger.exception("Exiting script!")
    exit()
finally:
    logger.info("Exiting script!")
    exit()

