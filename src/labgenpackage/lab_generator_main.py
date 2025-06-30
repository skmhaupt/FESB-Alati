from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.fill_groups import fill_groups
from labgenpackage.classes import Student
from labgenpackage.classes import Group
import logging
import enlighten
import xlsxwriter


def main(scraper_state: bool, mode: int, alf_prio_lvl: int):

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
            cours_participants: dict[str, Student] 
            cours_participants, _ = pars_cours_participants()
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
            logger.error('Failed parsing schedule!')
            raise

        #Get schedule for every student
        try:
            schedule_scraper(cours_participants, scraper_state)
            scraper_state = False
        except Exception:
            logger.error("Error when scraping schedule!")
            raise

        try:
            weight_generator(cours_participants, groups, alf_prio_lvl)
        except Exception:
            logger.error("Error generating starting weights!")
            raise
        
        try:
            successfule: bool = fill_groups(cours_participants, groups, mode)
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
            logger.error("Error filling groups!")
            raise
    
    counter = 0
    for student in cours_participants_copy.values():
        try:
            counter += 1
            logger.debug(f"{counter}:{student} is in group: {student.group}")
        except AttributeError:
            logger.warning(f"{counter}:{student} was not assigned a group. {student.fullname} can join groups: {student.groups}")
    
    logger.info("Execution recap:")
    for day in groups:
        for group in groups[day]:
            logger.info(f"Group: {group} filled with {len(group.students)} students.")
            logger.info(f"students: {*group.students,}")
            logger.info("------------------------------------------------------------------")

    workbook = xlsxwriter.Workbook("Filled_Groups.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write("A1", "Prezime")
    worksheet.write("B1", "Ime")
    worksheet.write("C1", "Email")
    worksheet.write("D1", "ID broj")
    worksheet.write("E1", "Korisničko ime")
    worksheet.write("F1", "Grupa")

    row: int = 2
    for student in cours_participants_copy.values():
        worksheet.write(f"A{row}", f"{student.surname}")
        worksheet.write(f"B{row}", f"{student.name}")
        worksheet.write(f"C{row}", f"{student.email}")
        worksheet.write(f"D{row}", f"{student.jmbag}")
        worksheet.write(f"E{row}", f"{student.username}")
        if hasattr(student, "group"):
            worksheet.write(f"F{row}", f"{student.group}")
        else:
            worksheet.write(f"F{row}", "Jos nisu svrstani")
        row += 1
    
    workbook.close()