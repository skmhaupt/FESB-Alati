from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.fill_groups import fill_groups
from labgenpackage.classes import Student
from labgenpackage.classes import Group
import logging
import enlighten


def main(scraper_state: bool):

    #Logger
    logger = logging.getLogger("my_app.main")

    # Setup progress bar
    manager = enlighten.get_manager()
    pbar = manager.counter(total=100, desc='Ticks', unit='ticks')

    running: bool = True
    counter: int = 0

    while running and counter<=100:
        logger.info(f"Now running attempt {counter}.")
        #Get cours participants
        try:
            logger.info("Starting participants parser!")
            cours_participants: dict[str, Student] = pars_cours_participants()
            cours_participants_copy: dict[str, Student] = cours_participants.copy()
            logger.info(f"Found {len(cours_participants)} students in participants file.")
        except TypeError:
            raise logger.exception("Failed parsing participants!")

        #Get lab group schedule
        try:
            logger.info("Starting schedule parser!")
            groups: dict[str, list:Group] = pars_schedule_file()
            numofgroups:int = 0
            day: str
            for day in groups:
                numofgroups += len(groups[day])
                logger.info(f"Found {len(groups[day])} groups for {day}")
            logger.info(f"Found {numofgroups} groups in total!")
        except Exception:
            raise logger.error('Failed parsing schedule!')

        #Get schedule for every student
        try:
            schedule_scraper(cours_participants, scraper_state)
        except Exception:
            raise logger.error("Error when scraping schedule!")

        try:
            weight_generator(cours_participants, groups)
        except Exception:
            raise logger.error("Error generating starting weights!")
        
        try:
            successfule: bool = fill_groups(cours_participants, groups)
            if successfule:
                running = False
                logger.info("Successfully filled out all groups with no students remaining!")
                for day in groups:
                    for group in groups[day]:
                        logger.info(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
                        logger.info("------------------------------------------------------------------")
            else:
                counter += 1
                pbar.update()
        except Exception:
            raise logger.error("Error filling groups!")

    for student in cours_participants_copy.values():
        logger.info(f"{student} is in group: {student.group}")
    #lowest: int = 9999999
    #counter: int = 0
    #for username in cours_participants:
    #    if cours_participants[username].weight < lowest:
    #        lowest = len(cours_participants[username].weight)
    #        counter = 1
    #   elif len(cours_participants[username].groups) == lowest: counter += 1
    #   print("User", username, "can join", len(cours_participants[username].groups), "groups!")
    #   print("Weight:", cours_participants[username].weight)
    #    #print("Can join groups:")
    #   #print(*cours_participants[username].groups, sep="\n")
    #    print("=====================================\n")

    #print(lowest)
    #print(counter)
    #for day in groups:
    #    print(*groups[day], sep="\n")