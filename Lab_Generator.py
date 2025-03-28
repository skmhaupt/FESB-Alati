import argparse
from labgenpackage.lab_generator_main import main

cli_parser = argparse.ArgumentParser(description='Create schedule for lab groups.')
cli_parser.add_argument("scraper_state", help="Enable or disable schedule scraper. Allowed inputs are: \"on\" and \"off\".")

args = cli_parser.parse_args()

if args.scraper_state == "off":
    scraper_state = False
elif args.scraper_state == "on":
    scraper_state = True

main(scraper_state)


