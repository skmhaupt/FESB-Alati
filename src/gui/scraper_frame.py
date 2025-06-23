from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.classes import Student
from threading import Thread
from pathlib import Path
from shutil import copy

import copy as listcopy
import customtkinter as ctk
import gui.settings as settings
import logging, xlsxwriter, os, json

# ScraperFrame crates the section used for getting the schedule of all students.
# This section is made around the 'schedule_scraper' funciton from 'labgenpackage'.
# All the scraped data is stored in 'src\Raspored_scraping\data\timetables'
class ScraperFrame(ctk.CTkFrame):
    def __init__(self, master, startdate:str, enddate:str, logger: logging.Logger):
        super().__init__(master)

        self.controller = master    # in case ctk widgets from other sections have to be accessed
        self.logger = logger

        self.section_title_label = ctk.CTkLabel(self, text="Raspored studenta", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 0), sticky="w")

        self.label_1 = ctk.CTkLabel(self, text="Preuzeti raspored u rasponu:")
        self.label_1.grid(row=1, column=0, padx=(10,0), pady=(10, 0), sticky="w")

        self.label_2 = ctk.CTkLabel(self, text="od - ")
        self.label_2.grid(row=1, column=1, padx=(5,0), pady=(10, 0), sticky="w")
        self.start_date_entry = ctk.CTkEntry(self, placeholder_text="dd.mm.yyyy")   # start date entry
        self.start_date_entry.configure(state="normal")
        self.start_date_entry.grid(row=1, column=2, padx=(0, 5), pady=(10, 0), sticky="we")

        self.label_3 = ctk.CTkLabel(self, text="do - ")
        self.label_3.grid(row=1, column=3, padx=(5,0), pady=(10, 0), sticky="w")
        self.end_date_entry = ctk.CTkEntry(self, placeholder_text="dd.mm.yyyy")     # end date entry
        self.end_date_entry.configure(state="normal")
        self.end_date_entry.grid(row=1, column=4, padx=(0, 5), pady=(10, 0), sticky="we")

        self.schedule_scrapper_button = ctk.CTkButton(self,width=60 , text="Preuzmi raspored", command=self.ScrapSchedule_setup)   # button to start the schedule scraper
        self.schedule_scrapper_button.grid(row=2, column=0, padx=(10,0), pady=10, sticky="")

        # subframe for satus display
        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=2, column=1, columnspan=4, padx=(5,5), pady=10,sticky="wens")
        self.subframe.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.subframe, text="Raspored studenta nije preuzet.")
        self.status_label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="")

        if not startdate=="":
            self.start_date_entry.insert(0,startdate)
        if not enddate=="":
            self.end_date_entry.insert(0,enddate)        

        self.Load_old_data()

    # 'Reset_label' is only called from 'ParticipantsFrame' and keeps the two sections in sync for clarity
    def Reset_label(self):
        settings.loaded_data[3] = False
        self.status_label.configure(text="Raspored studenta nije preuzet.", text_color="white")
        if hasattr(self, "details_button"):
            self.details_button.grid_remove()

    # 'Update_label' is used to load data from old session on startup
    def Load_old_data(self):
        # loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        settings.loaded_data[3] = False

        csvMissing = None
        csvEmpty = None

        try:
            if settings.cours_participants_global:
                cours_participants_local = listcopy.deepcopy(settings.cours_participants_global)    # work on deepcopy so the original doesnt have to be reset
                csvMissing, csvEmpty = schedule_scraper(cours_participants_local,False)   # false = get loaded data without running the scraper
                settings.loaded_data[3] = True
        except FileNotFoundError:
            self.logger.warning("No old data found on startup for schedule_scrapper.")
            return
        except ValueError:
            self.status_label.configure(text="Ucitani studenti nisu uskladeni sa preuzetim rasporedima za studente.", text_color="red")
            return
        except Exception as error:
            Errors: list[Student] = error.args[0]
            self.logger.error(f"Errors with users: {*Errors,}")
            self.status_label.configure(text="Nastala neocekivana pogreska!", text_color="red")
            return

        if csvMissing or csvEmpty:
            self.status_label.configure(text=f"Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}", text_color="white")
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text="Preuzmi detalje", command=lambda:self.ErrorDetails(csvMissing, csvEmpty))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
        elif settings.cours_participants_global:
            self.LoadedStatus(error="")
    
    # display status in subframe
    def LoadedStatus(self, error:str):
        if error=="":
            self.status_label.configure(text="Raspored studenta preuzet.", text_color="white")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        if error=="FileNotFoundError":
            self.status_label.configure(text="Pogreska! Nije zadana .csv datoteka sa studentima.", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        if error=="Exception":
            self.status_label.configure(text="Neocekivana pogreska!", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()

    # create excel file with error details
    def ErrorDetails(self, csvMissing:list[Student], csvEmpty:list[Student]):
        try:
            workbook = xlsxwriter.Workbook("data/Student_schedules_Error_detailes.xlsx")
            worksheet = workbook.add_worksheet()

            merge_format = workbook.add_format({"border":1, "bottom":5, "align": "center"})

            worksheet.write("A2", "Ime i prezime")
            worksheet.write("B2", "JMBAG")
            worksheet.write("C2", "E-Mail")

            worksheet.write("E2", "Ime i prezime")
            worksheet.write("F2", "JMBAG")
            worksheet.write("G2", "E-Mail")
            
            width1 = len("Ime i prezime")+1
            width2 = len("JMBAG")+1
            width3 = len("E-Mail")+1
            row: int = 3
            for student in csvMissing:
                worksheet.write(f"A{row}", f"{student.fullname}")
                if width1 < len(f"{student.fullname}"):
                    width1 = len(f"{student.fullname}")+1

                worksheet.write(f"B{row}", f"{student.jmbag}")
                if width2 < len(f"{student.jmbag}"):
                    width2 = len(f"{student.jmbag}")+1

                worksheet.write(f"C{row}", f"{student.email}")
                if width3 < len(f"{student.email}"):
                    width3 = len(f"{student.email}")+1

                row += 1

            worksheet.set_column(0, 0, width1)
            worksheet.set_column(1, 1, width2)
            worksheet.set_column(2, 2, width3)
            worksheet.merge_range("A1:C1", "Studenti kojima nije uspjesno preuzet raspored", merge_format)
            
            width1 = len("Ime i prezime")+1
            width2 = len("JMBAG")+1
            width3 = len("E-Mail")+1
            row: int = 3
            for student in csvEmpty:
                #worksheet.write(f"C{row}", f"{student}")
                worksheet.write(f"E{row}", f"{student.fullname}")
                if width1 < len(f"{student.fullname}"):
                    width1 = len(f"{student.fullname}")+1

                worksheet.write(f"F{row}", f"{student.jmbag}")
                if width2 < len(f"{student.jmbag}"):
                    width2 = len(f"{student.jmbag}")+1

                worksheet.write(f"G{row}", f"{student.email}")
                if width3 < len(f"{student.email}"):
                    width3 = len(f"{student.email}")+1

                row += 1

            worksheet.set_column(4, 4, width1)
            worksheet.set_column(5, 5, width2)
            worksheet.set_column(6, 6, width3)
            worksheet.merge_range("E1:G1", "Studenti kojima je preuzet raspored prazan", merge_format)

            workbook.close()

        except Exception:
            self.logger.critical("Error with creating Student_schedules_Error_detailes.xlsx")
            self.logger.exception()
        
        try:
            dest_dir = Path.home() / "Downloads"
            copy("data/Student_schedules_Error_detailes.xlsx", dest_dir)
            os.unlink("data/Student_schedules_Error_detailes.xlsx")
        except Exception:
            self.logger.exception("Error with downloading Student_schedules_Error_detailes.xlsx")
        
        self.details_button.configure(text="Preuzeto", text_color="green")
        self.details_button.after(2000, self.ResetDetailsButton)

    def ResetDetailsButton(self):
        self.details_button.configure(text="Preuzmi detalje", text_color="white")
    
    # Validate needed data before running scraper
    def ScrapSchedule_setup(self):
        #reset variable cours_participants_global
        settings.loaded_data[3] = False

        if not settings.cours_participants_global:
            self.logger.warning("Stoped schedule scraper.")
            self.LoadedStatus(error="FileNotFoundError")
            self.logger.info("Ending thread for scraping schedule.")
            settings.working = False
            return
        
        if settings.working:    # only one section can run at a time. This prevents unpredictable errors. - temporary fix
            self.logger.warning("Already runing another section! Cant upload new groups.")

            self.status_label.configure(text="Vec je pokrenuta druga sekcija.", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
            return
        
        else: settings.working = True   # block other sections from starting
        
        self.schedule_scrapper_button.grid_remove()
    
        # check if start and end date are valid dates
        startdate:str = self.start_date_entry.get()
        enddate:str = self.end_date_entry.get()
        if not self.ValidateDate(startdate):
            self.logger.warning(f"Entered invalid start date: {startdate}")
            self.status_label.configure(text="Pogreska sa prvim datumom.", text_color="red")
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        if not self.ValidateDate(enddate):
            self.logger.warning(f"Entered invalid end date: {enddate}")
            self.status_label.configure(text="Pogreska sa drugim datumom.", text_color="red")
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        self.logger.info(f"Entered valid dates: {startdate}, {enddate}")

        # pars start and end date
        dd,mm,yyyy=startdate.split(".")
        dd=int(dd)
        mm=int(mm)
        yyyy=int(yyyy)
        startdate = f"{dd:02}-{mm:02}-{yyyy:04}"
        jsonstartdate = f"{dd:02}.{mm:02}.{yyyy:04}"

        dd2,mm2,yyyy2=enddate.split(".")
        dd2=int(dd2)
        mm2=int(mm2)
        yyyy2=int(yyyy2)
        enddate = f"{dd2:02}-{mm2:02}-{yyyy2:04}"
        jsonenddate = f"{dd2:02}.{mm2:02}.{yyyy2:04}"

        # check if start date is older
        if not yyyy2 <= yyyy:
            pass
        elif not mm2 <= mm:
            pass
        elif not dd2 <= dd:
            pass
        else: 
            self.logger.warning("Start date is later than end date.")
            self.status_label.configure(text="Drugi datum je prije prvog.", text_color="red")
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        try:
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
                data["startdate"] = jsonstartdate
                data["enddate"] = jsonenddate
        except FileNotFoundError:   # if data.json is missing create new
            data = {"cours":"", "cours_number":"", "startdate":jsonstartdate, "enddate":jsonenddate}
        
        # save data to data.json
        json_object = json.dumps(data, indent=4)
        self.logger.info(f"Saving scraper dates: {jsonstartdate} - {jsonenddate}")
        with open("data/data.json", "w") as file:
            file.write(json_object)

        self.logger.info(f"Start date: {jsonstartdate}")
        self.logger.info(f"End date: {jsonenddate}")

        # progress bar for scrapper - will have to be improved
        self.SetProgressBar()
        self.scrapper_progressbar.start()

        # start the scraper thread
        scrapper_thread = Thread(target=self.ScrapeSchedule, args=(startdate,enddate))
        scrapper_thread.start()

    #scraper thread
    def ScrapeSchedule(self, startdate:str, enddate:str):
        self.logger.info("Started thread for scraping schedule.")

        cours_participants_local = listcopy.deepcopy(settings.cours_participants_global)    # work on deepcopy so the original doesnt have to be reset

        try:
            csvMissing, csvEmpty = schedule_scraper(cours_participants_local,True,startdate,enddate)    # true = run scraper and get loaded data
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            settings.loaded_data[3] = True
        except FileNotFoundError:   # csv file not loaded, this should never happen as it was already checked
            self.logger.warning("Stoped schedule scraper.")
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            self.LoadedStatus(error="FileNotFoundError")
            self.logger.info("Ending thread for scraping schedule.")
            self.schedule_scrapper_button.grid()
            settings.working = False
            return
        except Exception:
            self.logger.exception("Stoped schedule scraper.")
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.status_label.grid()
            self.LoadedStatus(error="Exception")
            self.logger.info("Ending thread for scraping schedule.")
            self.schedule_scrapper_button.grid()
            settings.working = False
            return

        # check if there are empty or missing csv files with scraped data
        if csvMissing or csvEmpty:
            self.status_label.configure(text=f"Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}", text_color="white")
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text="Preuzmi detalje", command=lambda:self.ErrorDetails(csvMissing, csvEmpty))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
        else:
            self.LoadedStatus(error="")
        
        self.schedule_scrapper_button.grid()
        settings.working = False
        self.logger.info("Ending thread for scraping schedule.")

    def SetProgressBar(self):
        self.status_label.grid_remove()
        if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        self.scrapper_progressbar = ctk.CTkProgressBar(self.subframe, orientation="horizontal", mode="determinate", determinate_speed=2)
        self.scrapper_progressbar.grid(row=0, column=0, padx=5, pady=10, sticky="we")

    def ValidateDate(self, date:str)->bool:
        if not len(date.split("."))==3:
            return False
        dd, mm, yyyy = date.split(".")
        if not dd.isdigit() or not 0 < int(dd) <= 31:
            self.logger.warning(f"Error with dd: {dd}")
            return False
        elif not mm.isdigit() or not 0 < int(mm) <= 12:
            self.logger.warning(f"Error with mm: {mm}")
            return False
        elif not yyyy.isdigit() or not 2024 < int(yyyy) < 2100:
            self.logger.warning(f"Error with yyyy: {yyyy}")
            return False
        else:
            return True