import logging, gui.settings as settings
from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_scraper import schedule_scraper

def FindeGroups(frame):
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
        csvMissing, csvEmpty = schedule_scraper(participatns,True,settings.start_date,settings.end_date)    # true = run scraper and get loaded data
    except FileNotFoundError:   # csv file not loaded, this should never happen as it was already checked
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
    

    print(participatns)
    print(csv_path)
    
    frame.DoneWorking()