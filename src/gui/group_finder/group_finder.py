from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.schedule_parser import schedule_parser_2
from excel_functions.found_appointments import GenFoundAppointmentsWorkbook

import logging, labgenpackage.find_groups as fg, gui.settings as settings

def FindeGroups(frame, start_date, end_date,timeslot_length:int,using_breaks:bool):
    from gui.group_finder.group_finder_frame import GroupFinderFrame
    frame: GroupFinderFrame = frame
    logger = logging.getLogger('my_app.group_finder')

    participatns = None
    try:
        logger.info("Loading participants from .csv file...")
        participatns, csv_path = pars_cours_participants("gui/group_finder/data")
        logger.info(f"Found {len(participatns)} students!")
        frame.status_label.configure(text="")
    except FileNotFoundError:
        logger.warning("File not founde.")
        participatns = None
        frame.DoneWorking()
        return
    except ValueError as error:
        csv_path = error.args[0]
        frame.status_label.configure(text="Neispravna datoteka.", text_color='red')
        frame.DoneWorking()
        return
    except Exception:
        logger.critical("Failed parcing participants!")
        frame.status_label.configure(text="Nastupila pogreska!", text_color='red')
        frame.DoneWorking()
        return
    

    try:
        timetables_dir = "gui/group_finder/data/timetables"
        schedule_scraper(cours_participants=participatns, dest_dir=timetables_dir, startdate=start_date, enddate=end_date)
        csvMissing, csvEmpty = schedule_parser_2(cours_participants=participatns, src_dir=timetables_dir)
    except FileNotFoundError:
        logger.critical("No participants uploaded for scrapper!")
        frame.status_label.configure(text="Nastupila neocekivana pogreska!", text_color='red')
        frame.DoneWorking()
        return
    except Exception as e:
        logger.critical("Unexpecter error!")
        logger.exception(e)
        frame.status_label.configure(text="Nastupila neocekivana pogreska!", text_color='red')
        frame.DoneWorking()
        return
    
    if csvMissing or csvEmpty:
        frame.status_label.configure(text=f'Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}', text_color='orange')
        # frame.details_button = ctk.CTkButton(frame.subframe,width=60 , text='Preuzmi detalje', command=lambda:frame.ErrorDetails(csvMissing, csvEmpty, logger))
        # frame.details_button.grid(row=1, column=0, padx=10, pady=10, sticky='')

    appointments_all_can_join = fg.FindeGroups(participatns, start_date, end_date, timeslot_length, using_breaks)
    
    cours_name = frame.controller.cours_frame.cours_name_entry.get()
    cours_number = frame.controller.cours_frame.cours_number_entry.get()
    acad_year = frame.controller.cours_frame.year_entry.get()

    try:
        GenFoundAppointmentsWorkbook(appointments_all_can_join,cours_name, cours_number, acad_year)
    except Exception as e:
        logger.exception(e)

    frame.DoneWorking()