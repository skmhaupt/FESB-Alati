from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.schedule_parser import Group
import traceback
import logging


def main(scraper_state: bool):
    #Get cours participants
    try:
        cours_participants = pars_cours_participants()
        print('Found', len(cours_participants), 'students in participants file.')
    except TypeError:
        print('Exiting script from participants parsing!')
        exit()

    #Get lab group schedule
    try:
        groups: dict[str, list:Group] = pars_schedule_file()
        print('Found', len(groups), 'groups in schedule file.')
    except Exception as e:
        print('Exiting script from schedule parsing!')
        print(e)
        logging.error(traceback.format_exc)
        return e

    #Get schedule for every student
    try:
        schedule_scraper(cours_participants, scraper_state)
    except Exception as e:
        print("Error when scraping schedule!")
        print("Exception: ", e)
        exit()

    weight_generator(cours_participants, groups)

    lowest: int = 300
    counter = 0
    for username in cours_participants:
        if len(cours_participants[username].groups) < lowest:
            lowest = len(cours_participants[username].groups)
            counter = 1
        elif len(cours_participants[username].groups) == lowest: counter += 1
        print("User", username, "can join", len(cours_participants[username].groups), "groups!")
        print("Weight:", cours_participants[username].weight)
        #print("Can join groups:")
        #print(*cours_participants[username].groups, sep="\n")
        print("=====================================\n")

    print(lowest)
    print(counter)