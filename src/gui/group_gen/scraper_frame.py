from excel_functions.fill_groups_results import GenScraperDetailesWorkbook
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.schedule_parser import schedule_parser
from labgenpackage.classes import Student
from threading import Thread
from gui.util import ValidateDate
# from pathlib import Path
# from shutil import copy

import copy as listcopy
import customtkinter as ctk
import gui.settings as settings, gui.util as util
import logging, os, json, re

# ScraperFrame crates the section used for getting the schedule of all students.
# This section is made around the 'schedule_scraper' funciton from 'labgenpackage'.
# All the scraped data is stored in 'src\Raspored_scraping\data\timetables'
class ScraperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        logger = logging.getLogger('my_app.group_gen.scraper')
        logger.setLevel('INFO')

        self.v_date = (self.register(self.date_callback))

        self.section_title_label = ctk.CTkLabel(self, text='Raspored studenta', font=('Helvetica', 23))
        self.section_title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 0), sticky='w')

        self.label_1 = ctk.CTkLabel(self, text='Preuzeti raspored u rasponu:')
        self.label_1.grid(row=1, column=0, padx=(10,0), pady=(10, 0), sticky='w')

        self.label_2 = ctk.CTkLabel(self, text='od - ')
        self.label_2.grid(row=1, column=1, padx=(5,0), pady=(10, 0), sticky='w')
        self.start_date_entry = ctk.CTkEntry(self, validate='all')
        self.start_date_entry.grid(row=1, column=2, padx=(0, 5), pady=(10, 0), sticky='we')
        self.start_date_entry.configure(placeholder_text='dd.mm.yyyy', validatecommand=(self.v_date, '%P', self.start_date_entry))

        self.label_3 = ctk.CTkLabel(self, text='do - ')
        self.label_3.grid(row=1, column=3, padx=(5,0), pady=(10, 0), sticky='w')
        self.end_date_entry = ctk.CTkEntry(self, validate='all')
        self.end_date_entry.grid(row=1, column=4, padx=(0, 10), pady=(10, 0), sticky='we')
        self.end_date_entry.configure(placeholder_text='dd.mm.yyyy', validatecommand=(self.v_date, '%P', self.end_date_entry))

        self.schedule_scrapper_button = ctk.CTkButton(self,width=60 , text='Preuzmi raspored', command=self.ScrapSchedule_setup)
        self.schedule_scrapper_button.grid(row=2, column=0, padx=(10,0), pady=10, sticky='')

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=2, column=1, columnspan=4, padx=10, pady=10,sticky='wens')
        self.subframe.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.subframe, text='Raspored studenta nije preuzet.')
        self.status_label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky='')

        if not settings.start_date=='':
            self.start_date_entry.insert(0,settings.start_date)
        if not settings.end_date=='':
            self.end_date_entry.insert(0,settings.end_date)        

        self.Load_old_data()

    # ------------------------------------------
    def date_callback(self, P, entry: str):
        entry:ctk.CTkEntry = self.nametowidget(entry)
        old_len = 0
        old_len = len(entry.get())
        if P == 'dd.mm.yyyy': return True
        if re.fullmatch('[0-9]{0,1}', P): return True
        elif re.fullmatch('[0-9]{2}', P):
            if old_len < 2:
                entry.after(1, lambda: entry.insert(3,'.'))
            elif old_len > 2:
                entry.after(1, lambda: entry.delete(1,ctk.END))
            return True
        elif re.fullmatch('[0-9]{2}.[0-9]{0,1}', P): return True
        elif re.fullmatch('[0-9]{2}.[0-9]{2}', P):
            if old_len < 5:
                entry.after(1, lambda: entry.insert(6,'.'))
            elif old_len > 5:
                entry.after(1, lambda: entry.delete(4,ctk.END))
            return True
        elif re.fullmatch('[0-9]{2}.[0-9]{2}.[0-9]{0,4}', P): return True
        else: return False

    # ------------------------------------------
    # 'Reset_label' is only called from 'ParticipantsFrame' and keeps the two sections in sync for clarity
    def Reset_label(self):
        settings.loaded_data[3] = False
        self.status_label.configure(text='Raspored studenta nije preuzet.', text_color='white')
        if hasattr(self, 'details_button'):
            self.details_button.grid_remove()

    # ------------------------------------------
    # 'Update_label' is used to load data from old session on startup
    def Load_old_data(self):
        logger = logging.getLogger('my_app.group_gen.scraper')

        # loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        settings.loaded_data[3] = False

        csvMissing = None
        csvEmpty = None

        try:
            if settings.cours_participants_global:
                logger.info('Loading old data...')
                cours_participants_local = listcopy.deepcopy(settings.cours_participants_global)    # work on deepcopy so the original doesnt have to be reset
                csvMissing, csvEmpty = schedule_parser(cours_participants_local,'data/timetables')   # false = get loaded data without running the scraper
                settings.loaded_data[3] = True
        except FileNotFoundError:
            logger.warning('No old data found on startup for schedule_scrapper.')
            return
        except ValueError:
            self.status_label.configure(text='Ucitani studenti nisu uskladeni sa preuzetim rasporedima za studente.', text_color='red')
            return
        except Exception as error:
            Errors: list[Student] = error.args[0]
            logger.error(f'Errors with users: {*Errors,}')
            self.status_label.configure(text='Nastala neocekivana pogreska!', text_color='red')
            return

        if csvMissing or csvEmpty:
            logger.warning('Potential errors.')
            self.status_label.configure(text=f'Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}', text_color='white')
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text='Preuzmi detalje', command=lambda:self.ErrorDetails(csvMissing, csvEmpty,logger))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky='')
        elif settings.cours_participants_global:
            self.LoadedStatus(error='')
    
    # ------------------------------------------
    # display status in subframe
    def LoadedStatus(self, error:str):
        if error=='':
            self.status_label.configure(text='Raspored studenta preuzet.', text_color='white')
            if hasattr(self, 'details_button'):
                self.details_button.grid_remove()
        if error=='FileNotFoundError':
            self.status_label.configure(text='Pogreska! Nije zadana .csv datoteka sa studentima.', text_color='red')
            if hasattr(self, 'details_button'):
                self.details_button.grid_remove()
        if error=='Exception':
            self.status_label.configure(text='Neocekivana pogreska!', text_color='red')
            if hasattr(self, 'details_button'):
                self.details_button.grid_remove()

    # ------------------------------------------
    # create excel file with error details
    def ErrorDetails(self, csvMissing:list[Student], csvEmpty:list[Student], logger:logging.Logger):
        try:
            GenScraperDetailesWorkbook(csvMissing, csvEmpty)
        except Exception:
            logger.critical('Error with creating Student_schedules_Error_detailes.xlsx')
            raise
        
        try:
            util.CopyAndRename(srcname='Student_schedules_Error_detailes.xlsx', dstname='Greske_sa_preuzetim_rasporedima')
            os.unlink('data/Student_schedules_Error_detailes.xlsx')
        except Exception:
            logger.exception('Error with downloading Student_schedules_Error_detailes.xlsx')
        
        self.details_button.configure(text='Preuzeto', text_color='green')
        self.details_button.after(2000, lambda: util.ResetButton(self.details_button, 'Preuzmi detalje', 'white'))
    
    # ------------------------------------------
    def ScrapSchedule_setup(self):
        logger = logging.getLogger('my_app.group_gen.scraper')

        settings.loaded_data[3] = False

        if not settings.cours_participants_global:
            logger.warning('Stoped schedule scraper.')
            self.LoadedStatus(error='FileNotFoundError')
            settings.working = False
            return
        
        if settings.working:    # only one section can run at a time. This prevents unpredictable errors. - temporary fix
            logger.warning('Already runing another section! Cant upload new groups.')

            self.status_label.configure(text='Vec je pokrenuta druga sekcija.', text_color='red')
            if hasattr(self, 'details_button'):
                self.details_button.grid_remove()
            return
        
        else: settings.working = True   # block other sections from starting
        
        self.schedule_scrapper_button.grid_remove()
    
        start_date:str = self.start_date_entry.get()
        end_date:str = self.end_date_entry.get()
        
        valid, dd, mm, yyyy = ValidateDate(start_date,logger)
        valid2, dd2, mm2, yyyy2 = ValidateDate(end_date,logger)
        
        if not valid:
            logger.warning(f'Entered invalid start date: {start_date}')
            self.status_label.configure(text='Pogreska sa prvim datumom.', text_color='red')
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        if not valid2:
            logger.warning(f'Entered invalid end date: {end_date}')
            self.status_label.configure(text='Pogreska sa drugim datumom.', text_color='red')
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        logger.info(f'Entered valid dates: {start_date}, {end_date}')

        start_date = f'{dd:02}-{mm:02}-{yyyy:04}'
        jsonstartdate = f'{dd:02}.{mm:02}.{yyyy:04}'
        end_date = f'{dd2:02}-{mm2:02}-{yyyy2:04}'
        jsonenddate = f'{dd2:02}.{mm2:02}.{yyyy2:04}'

        if not yyyy2 <= yyyy:
            pass
        elif not mm2 <= mm:
            pass
        elif not dd2 <= dd:
            pass
        else: 
            logger.warning('Start date is later than end date.')
            self.status_label.configure(text='Drugi datum je prije prvog.', text_color='red')
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        
        settings.end_date = end_date
        settings.start_date = start_date
        
        try:
            with open('data/data.json', 'r') as file:
                data:dict[str:str] = json.load(file)
        except FileNotFoundError:   # if data.json is missing create new
            data = settings.default_data_json
        finally:
                data['start_date'] = jsonstartdate
                data['end_date'] = jsonenddate
        
        # save data to data.json
        json_object = json.dumps(data, indent=4)
        logger.info(f'Saving scraper dates: {jsonstartdate} - {jsonenddate}')
        with open('data/data.json', 'w') as file:
            file.write(json_object)

        logger.info(f'Start date: {jsonstartdate}')
        logger.info(f'End date: {jsonenddate}')

        # progress bar for scrapper - will have to be improved
        self.SetProgressBar()
        self.scrapper_progressbar.start()

        # start the scraper thread
        scrapper_thread = Thread(target=self.ScrapeSchedule)
        scrapper_thread.start()

    # ------------------------------------------
    #scraper thread
    def ScrapeSchedule(self):
        logger = logging.getLogger('my_app.group_gen.scraper')

        logger.info('Scraping schedule...')

        cours_participants_local = listcopy.deepcopy(settings.cours_participants_global)    # work on deepcopy so the original doesnt have to be reset

        try:
            schedule_scraper(cours_participants_local,'data/timetables',settings.start_date,settings.end_date)
            csvMissing, csvEmpty = schedule_parser(cours_participants_local,'data/timetables')
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            settings.loaded_data[3] = True
        except FileNotFoundError:   # csv file not loaded, this should never happen as it was already checked
            logger.warning('Stoped schedule scraper.')
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            self.LoadedStatus(error='FileNotFoundError')
            logger.info('Ending thread for scraping schedule.')
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        except Exception:
            logger.exception('Stoped schedule scraper.')
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            self.LoadedStatus(error='Exception')
            logger.info('Ending thread for scraping schedule.')
            self.schedule_scrapper_button.grid()
            settings.working = False
            return

        # check if there are empty or missing csv files with scraped data
        if csvMissing or csvEmpty:
            self.status_label.configure(text=f'Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}', text_color='white')
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text='Preuzmi detalje', command=lambda:self.ErrorDetails(csvMissing, csvEmpty, logger))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky='')
        else:
            self.LoadedStatus(error='')
        
        self.schedule_scrapper_button.grid()
        settings.working = False
        logger.info('Scraped schedule.')
        logger.info('Ending thread for scraping schedule.')

    # ------------------------------------------
    def SetProgressBar(self):
        self.status_label.grid_remove()
        if hasattr(self, 'details_button'):
                self.details_button.grid_remove()
        self.scrapper_progressbar = ctk.CTkProgressBar(self.subframe, orientation='horizontal', mode='determinate', determinate_speed=2)
        self.scrapper_progressbar.grid(row=0, column=0, padx=5, pady=10, sticky='we')