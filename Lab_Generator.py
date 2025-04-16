import argparse
from labgenpackage.lab_generator_main import main
import traceback
import logging

#Logger setup
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
#console logger
formatter = logging.Formatter(
   "{levelname}-{name}:{message}",
    style="{"
)
console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.info("App started.")
#file logger
# formatter = logging.Formatter(
#    "{levelname}-{name}:{message}",
#     style="{"
# )
#file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
#file_handler.setLevel("WARNING")
#file_handler.setFormatter(formatter)
#logger.addHandler(file_handler)


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
except Exception:
    logging.exception("Error")

