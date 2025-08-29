from gui.group_finder.group_finder import FindeGroups
from gui.util import ValidateDate, DelOldFile
from pathlib import Path
from shutil import copy

import logging, gui.settings as settings

def GroupFinder_setup(frame):
    from gui.group_finder.group_finder_frame import GroupFinderFrame
    
    frame: GroupFinderFrame = frame
    logger = logging.getLogger('my_app.group_finder')
    
    frame.finde_groups_button.grid_remove()
    frame.SetProgressBar()
    frame.progressbar.start()

    if settings.working:    # only one section can run at a time. This prevents unpredictable errors. - temporary fix
        logger.warning('Already runing another section! Cant upload new groups.')
        frame.status_label.configure(text='Vec je pokrenuta druga sekcija.', text_color='red')
        frame.finde_groups_button.grid()
        return
    else: settings.working = True   # block other sections from starting

    participants = frame.csv_file_entry.get()
    if not participants:
        logger.warning('No .csv file provided.')
        frame.status_label.configure(text='Nije zadana datoteka sa studentima.', text_color='red')
        frame.DoneWorking(error=True)
        return
    elif not participants.endswith(".csv"):
        logger.warning('Provided file is not a csv. file')
        frame.status_label.configure(text='Zadana datoteka mora biti .csv formata.', text_color='red')
        frame.DoneWorking(error=True)
        return
    else:
        fpath = Path(participants)
        data_dir = 'gui/group_finder/data'
        try:
            DelOldFile(data_dir,'csv', logger)
            copy(fpath, data_dir)
            logger.info(f'Uploaded new file: {fpath}!')
        except Exception as e:
            logger.critical(f'Failed to upload new file: {fpath}!')
            logger.exception(e)
            frame.status_label.configure(text='Neocekivana pogreska.', text_color='red')
            frame.DoneWorking(error=True)
            return

    start_date:str = frame.start_date_entry.get()
    end_date:str = frame.end_date_entry.get()
    valid, dd, mm, yyyy = ValidateDate(start_date,logger)
    valid2, dd2, mm2, yyyy2 = ValidateDate(end_date,logger)
    if not valid:
        logger.warning(f'Entered invalid start date: {start_date}')
        frame.status_label.configure(text='Pogreska sa prvim datumom.', text_color='red')
        frame.DoneWorking(error=True)
        return
    if not valid2:
        logger.warning(f'Entered invalid end date: {end_date}')
        frame.status_label.configure(text='Pogreska sa drugim datumom.', text_color='red')
        frame.DoneWorking(error=True)
        return
    if not yyyy2 <= yyyy: pass
    elif not mm2 <= mm: pass
    elif not dd2 <= dd: pass
    else: 
        logger.warning('Start date is later than end date.')
        frame.status_label.configure(text='Drugi datum je prije prvog.', text_color='red')
        frame.DoneWorking(error=True)
        return
    logger.info(f'Entered valid dates: {start_date}, {end_date}')
    start_date = f'{dd:02}-{mm:02}-{yyyy:04}'
    end_date = f'{dd2:02}-{mm2:02}-{yyyy2:04}'

    timeslot_length = frame.timeslot_length_entry.get()
    if not timeslot_length: 
        logger.warning('No timeslot length provided.')
        frame.status_label.configure(text='Treba zadati broj potrebnih sati.', text_color='red')
        frame.DoneWorking(error=True)
        return
    using_breaks = frame.using_breaks.get()

    FindeGroups(frame, start_date, end_date, int(timeslot_length), using_breaks)