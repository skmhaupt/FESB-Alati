from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.schedule_parser import schedule_parser_2
from excel_functions.found_appointments import GenFoundAppointmentsWorkbook
from excel_functions.fill_groups_results import GenScraperDetailesWorkbook
from labgenpackage.classes import Student

import os, logging, labgenpackage.find_groups as fg, customtkinter as ctk, gui.util as util, gui.settings as settings

def FindeGroups(frame, start_date, end_date,timeslot_length:int,using_breaks:bool):
    from gui.group_finder.group_finder_frame import GroupFinderFrame
    frame: GroupFinderFrame = frame
    logger = logging.getLogger('my_app.group_finder')

    participatns = None
    try:
        logger.info("Loading participants from .csv file...")
        participatns, csv_path = pars_cours_participants("data/group_finder")
        logger.info(f"Found {len(participatns)} students!")
        frame.status_label.configure(text="")
    except FileNotFoundError:
        logger.warning("File not founde.")
        participatns = None
        frame.DoneWorking(error=True)
        return
    except ValueError as error:
        csv_path = error.args[0]
        frame.status_label.configure(text="Neispravna datoteka.", text_color='red')
        frame.DoneWorking(error=True)
        return
    except Exception:
        logger.critical("Failed parcing participants!")
        frame.status_label.configure(text="Nastupila pogreska!", text_color='red')
        frame.DoneWorking(error=True)
        return
    

    try:
        timetables_dir = "data/group_finder/timetables"
        schedule_scraper(cours_participants=participatns, dest_dir=timetables_dir, startdate=start_date, enddate=end_date)
        csvMissing, csvEmpty = schedule_parser_2(cours_participants=participatns, src_dir=timetables_dir)
    except FileNotFoundError:
        logger.critical("No participants uploaded for scrapper!")
        frame.status_label.configure(text="Nastupila neocekivana pogreska!", text_color='red')
        frame.DoneWorking(error=True)
        return
    except Exception as e:
        logger.critical("Unexpecter error!")
        logger.exception(e)
        frame.status_label.configure(text="Nastupila neocekivana pogreska!", text_color='red')
        frame.DoneWorking(error=True)
        return
    
    if csvMissing or csvEmpty:
        frame.status_label.configure(text=f'Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}', text_color='orange')
        ErrorDetails(csvMissing, csvEmpty, logger)

    appointments_all_can_join = fg.FindeGroups(participatns, start_date, end_date, timeslot_length, using_breaks)
    
    cours_name = frame.controller.cours_frame.cours_name_entry.get()
    cours_number = frame.controller.cours_frame.cours_number_entry.get()
    acad_year = frame.controller.cours_frame.year_entry.get()

    try:
        GenFoundAppointmentsWorkbook(appointments_all_can_join, cours_name, cours_number, acad_year)
        frame.num_of_groups_label.configure(text=f'Broj dostupnih grupa: {len(appointments_all_can_join)}')
        old_status_txt = frame.status_label._text
        if old_status_txt:
            frame.status_label.configure(text=f"{old_status_txt}\nPreuzeta datoteka sa terminima i datoteka sa mogucim pogreskama!")
        else:
            frame.status_label.configure(text="Preuzeta datoteka!", text_color='green')
        frame.DoneWorking(error=False)
    except Exception as e:
        logger.exception(e)
        frame.status_label.configure(text="Nastupila neocekivana pogreska pri generiranju excel datoteke!", text_color='red')
        frame.DoneWorking(error=True)
        return

def ErrorDetails(csvMissing:list[Student], csvEmpty:list[Student], logger:logging.Logger):
        try:
            GenScraperDetailesWorkbook(csvMissing, csvEmpty)
        except Exception:
            logger.critical('Error with creating Student_schedules_Error_detailes.xlsx')
            raise
        
        try:
            util.CopyAndRename(srcpath='data/Student_schedules_Error_detailes.xlsx', dstname='Greske_sa_preuzetim_rasporedima')
            os.unlink('data/Student_schedules_Error_detailes.xlsx')
        except Exception:
            logger.exception('Error with downloading Student_schedules_Error_detailes.xlsx')