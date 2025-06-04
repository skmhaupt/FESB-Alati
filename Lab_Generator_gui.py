from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.classes import CustomFormatter
from labgenpackage.fill_groups import fill_groups
from labgenpackage.classes import Student
from labgenpackage.classes import Group
from customtkinter import filedialog
from threading import Thread
from pathlib import Path
from shutil import copy, move
import copy as copydict
from os import path
import customtkinter as ctk
import logging.config
import logging
import xlsxwriter
import json
import glob
import os

#Logger setup
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
     "formatters": {
         "simple": {
             "format": "{levelname} - {name}: {message}",
             "style":"{"
         }
     },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            #"formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "debug_rotating_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "filename": "debug.log",
            "maxBytes": 150000,
            "backupCount": 3,
            "encoding":"utf-8"
        }
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout", "debug_rotating_file_handler"]}
    }
}
logging.config.dictConfig(config=logging_config)
ch = logging.getHandlerByName("stdout")
ch1 = logging.getHandlerByName("debug_rotating_file_handler")
ch.setFormatter(CustomFormatter())
ch1.setFormatter(CustomFormatter())
logger = logging.getLogger("my_app")


class GroupsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.label_1 = ctk.CTkLabel(self, text="Grupe", font=("Helvetica", 23))
        self.label_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="we")

        self.label_2 = ctk.CTkLabel(self, text="Ulazna datoteka:")
        self.label_2.grid(row=1, column=0, padx=(10,5), pady=(10, 0), sticky="we")

        self.entry_1 = ctk.CTkEntry(self, width=100, placeholder_text=".txt datoteka")
        self.entry_1.configure(state="readonly")
        self.entry_1.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0, 0), sticky="we")
        self.button_1 = ctk.CTkButton(self,width=60 , text="Pretrazi", command=self.BrowseAction)
        self.button_1.grid(row=2, column=2, padx=(0, 10), pady=(0, 0), sticky="we")

        self.button_2 = ctk.CTkButton(self,width=125 , text="Ucitaj datoteku", command=self.UploadAction)
        self.button_2.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="")

        self.label_loaded_schedule = ctk.CTkLabel(self, text="Nije ucitan raspored grupa.")    
        self.label_loaded_schedule.grid(row=4, column=0,columnspan=3, padx=(10,0), pady=(10, 0), sticky="")
        self.label_num_of_groups = ctk.CTkLabel(self, text="Broj grupa: N/A")
        self.label_num_of_groups.grid(row=5, column=0, padx=(10,0), pady=0, sticky="")
        self.label_num_of_places = ctk.CTkLabel(self, text="Broj dostupnih mjesta: N/A")
        self.label_num_of_places.grid(row=5, column=1, columnspan=2, padx=(0,20), pady=0, sticky="")

        self.subframe = ctk.CTkScrollableFrame(self)
        self.subframe.grid(row=6, column=0, columnspan=3, padx=10, pady=(0,10),sticky="wens")
        self.label_3 = ctk.CTkLabel(self.subframe, text="Grupe nisu ucitane.")
        self.label_3.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="we")
        try:
            self.LoadGroups()
        except FileNotFoundError:
            return
        except Exception:
            logger.error("Error when loading groups on startup!")
            raise
    
    def LoadGroups(self)->str:
        global total_places, loaded_data
        total_places = 0

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        loaded_data[0] = False

        try:
            groups, filename = pars_schedule_file()
        except ValueError:
            self.NoGroupsInUploadedFile()
            return
        except FileNotFoundError:
            raise
        except Exception:
            logger.error("Failed parcing participants!")
            raise

        for widget in self.subframe.winfo_children():
            widget.destroy()  # deleting widget

        row:int = 2
        
        group:Group
        for groups_in_day in groups.values():
            for group in groups_in_day:
                self.AddGrouplabel(row,group)
                total_places+=group.group_size
                row+=1
        logger.info(f"Found {row-2} groups. With {total_places} places in total.")
        
        self.label_loaded_schedule.configure(text=f"Ucitani raspored: {filename}")
        self.label_num_of_groups.configure(text=f"Broj grupa: {row-2}")
        self.label_num_of_places.configure(text=f"Broj dostupnih mjesat: {total_places}")
        loaded_data[0] = True

    
    def NoGroupsInUploadedFile(self):
        self.label_loaded_schedule.configure(text=f"Nije ucitan raspored grupa.")
        self.label_num_of_groups.configure(text=f"Broj grupa: N/A")
        self.label_num_of_places.configure(text=f"Broj dostupnih mjesta: N/A")

        for widget in self.subframe.winfo_children():
            widget.destroy()  # deleting widget

        self.warning_label = ctk.CTkLabel(self.subframe, text=f"Ispravni format zapisa grupa u datoteci:", text_color="red")
        self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label2 = ctk.CTkLabel(self.subframe, text=f"grupa, dan, od - do, dvorana, broj studenta")
        self.warning_label2.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label3 = ctk.CTkLabel(self.subframe, text=f"G1, PON, 09:30 - 11:00, B419, 12")
        self.warning_label3.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label4 = ctk.CTkLabel(self.subframe, text=f"G2, UTO, 09:30 - 11:00, B419, 12")
        self.warning_label4.grid(row=5, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label5 = ctk.CTkLabel(self.subframe, text=f"GC, SRI, 09:30 - 11:00, B419, 12")
        self.warning_label5.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label6 = ctk.CTkLabel(self.subframe, text=f"GD, ČET, 09:30 - 11:00, B419, 12")
        self.warning_label6.grid(row=7, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label7 = ctk.CTkLabel(self.subframe, text=f"Grupa5, PET, 09:30 - 11:00, B419, 12")
        self.warning_label7.grid(row=8, column=0, padx=5, pady=(5, 0), sticky="w")

    def AddGrouplabel(self, row:int, group:Group):
        self.group_label1 = ctk.CTkLabel(self.subframe, text=f"{group.group_label}")
        self.group_label1.grid(row=row, column=0, padx=5, pady=(5, 0), sticky="we")
        self.group_label2 = ctk.CTkLabel(self.subframe, text=f"{group.day}")
        self.group_label2.grid(row=row, column=1, padx=5, pady=(5, 0), sticky="we")
        self.group_label3 = ctk.CTkLabel(self.subframe, text=f"{group.time}")
        self.group_label3.grid(row=row, column=2, padx=5, pady=(5, 0), sticky="we")
        self.group_label4 = ctk.CTkLabel(self.subframe, text=f"{group.lab}")
        self.group_label4.grid(row=row, column=3, padx=5, pady=(5, 0), sticky="we")
        self.group_label5 = ctk.CTkLabel(self.subframe, text=f"{group.group_size}")
        self.group_label5.grid(row=row, column=4, padx=5, pady=(5, 0), sticky="we")

    def BrowseAction(self):
        filename = filedialog.askopenfilename()
        self.entry_1.configure(state="normal")
        self.entry_1.delete(0, "end")
        self.entry_1.insert(0,filename)
        self.entry_1.configure(state="readonly")
        logger.info(f"Selected file: {filename}")

    def UploadAction(self):
        input_txt_file = self.entry_1.get()
        if(input_txt_file==""):
            logger.warning("Select a .txt file befor uploading.")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Nije zadana .txt datoteka.", text_color="red")
            self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return
        elif input_txt_file.endswith(".txt"):
            logger.info(f"{self.entry_1.get()}")
        else:
            logger.warning("Input file hase to be a .txt file.")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Odabrana pogresna datoteka.", text_color="red")
            self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return
        
        #get path to old existing .txt file
        fpath: Path
        fpaths: list = glob.glob("data/*.txt")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} old .txt files, there has to be only one!")
            logger.critical(f"Erasing all \'.txt\' files!")
            for pathstr in fpaths:
                logger.critical(f"Erasing {pathstr}")
                delpath = Path(pathstr)
                delpath.unlink()
        elif(len(fpaths) == 0):
            logger.info("No old .txt file found!")
        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                logger.info(f"Deleted old .txt file {fpath}!")
            except Exception:
                logger.critical(f"Failed to delete old txt file {fpath}")
                for widget in self.subframe.winfo_children():
                    widget.destroy()  # deleting widget
                    self.warning_label = ctk.CTkLabel(self.subframe, text=f"Neocekivana pogreska.\nPokusajte ponovo.", text_color="red")
                    self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
                return
        
        #get new selected .txt file
        fpath = Path(input_txt_file)
        try:
            copy(fpath, "data/")
            logger.info(f"Uploaded new file: {fpath}!")
        except Exception:
            logger.critical(f"Failed to copy new file: {fpath}!")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
                self.warning_label = ctk.CTkLabel(self.subframe, text=f"Neocekivana pogreska.\nPokusajte ponovo.", text_color="red")
                self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return

        self.LoadGroups()

#Contains the right side of the UI: CoursFrame, ParticipantsFrame, ...
class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(1, weight=1)
        #self.grid_rowconfigure(2, weight=1)
        #self.grid_rowconfigure(3, weight=1)

        #Expected data is dict {"cours", "cours_number", "startdate", "enddate"}
        try:
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
        except FileNotFoundError:
            logger.warning("The file 'data/data.json' was not found.")
            data = {"cours":"", "cours_number":"", "startdate":"","enddate":""}
            pass
        except IOError:
            logger.critical("Error opening data.json file!")
            raise
        except Exception:
            logger.critical("Unexpected error with data.jsonfile !")
            raise
            

        self.cours_frame = CoursFrame(self,data["cours"], data["cours_number"])
        self.cours_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.participants_frame = ParticipantsFrame(self)
        self.participants_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.scraper_frame = ScraperFrame(self,data["startdate"], data["enddate"])
        self.scraper_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.fill_groups_frame = FillGroupsFrame(self)
        self.fill_groups_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


#First segment of the right side of the UI. Hold the section for cours data
class CoursFrame(ctk.CTkFrame):
    def __init__(self, master, cours_name, cours_number):
        super().__init__(master)
        self.label_1 = ctk.CTkLabel(self, text="Predmet:")
        self.label_1.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="w")
        self.cours_name_entry = ctk.CTkEntry(self, placeholder_text="npr: PDS, SDOS, itd.")
        self.cours_name_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="e")

        self.label_2 = ctk.CTkLabel(self, text="Smjer:")
        self.label_2.grid(row=0, column=2, padx=(10, 5), pady=(10, 10), sticky="w")
        self.cours_number_entry = ctk.CTkEntry(self, placeholder_text="npr: 112, 222 itd.")
        self.cours_number_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10), sticky="e")

        if not cours_name=="":
            self.cours_name_entry.insert(0,cours_name)
        if not cours_number=="":
            self.cours_number_entry.insert(0,cours_number)

class ParticipantsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = master

        self.grid_columnconfigure(1, weight=1)

        self.label_1 = ctk.CTkLabel(self, text="Sudionici", font=("Helvetica", 23))
        self.label_1.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")

        self.label_2 = ctk.CTkLabel(self, text="Ulazna datoteka:")
        self.label_2.grid(row=1, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
        self.entry_1 = ctk.CTkEntry(self, width=500, placeholder_text=".csv datoteka")
        self.entry_1.configure(state="readonly")
        self.entry_1.grid(row=1, column=1, padx=(0, 5), pady=(10, 0), sticky="we")
        self.button_1 = ctk.CTkButton(self,width=60 , text="Pretrazi", command=self.BrowseAction)
        self.button_1.grid(row=1, column=2, padx=(0, 10), pady=(10, 0), sticky="e")

        self.button_2 = ctk.CTkButton(self,width=125 , text="Ucitaj datoteku", command=self.UploadAction)
        self.button_2.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="")
        self.label_error = ctk.CTkLabel(self, text="")
        self.label_error.grid(row=2, column=1, columnspan=2, padx=10, pady=(10, 0), sticky="w")

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=3, column=0, columnspan=3, padx=10, pady=10,sticky="")
        self.label_3 = ctk.CTkLabel(self.subframe, text="Ucitana datoteka:")
        self.label_3.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
        self.label_4 = ctk.CTkLabel(self.subframe, text="Trenutno nije ucitana .csv datoteka!")
        self.label_4.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="w")
        self.label_5 = ctk.CTkLabel(self.subframe, text="Broj ucitanih studenta:")
        self.label_5.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="w")
        self.label_6 = ctk.CTkLabel(self.subframe, text="Trenutno nije ucitana .csv datoteka!")
        self.label_6.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="w")

        self.first_load = True
        self.LoadParticipants()
        self.first_load = False
        

    def LoadParticipants(self):
        global cours_participants_global, loaded_data

        cours_participants_global = None

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        loaded_data[2] = False

        try:
            cours_participants_global, fpath = pars_cours_participants()
            logger.info(f"Found {len(cours_participants_global)} students!")
            self.label_error.configure(text="")
        except FileNotFoundError:
            logger.warning("File not founde. Returning from LoadParticipants()!")
            cours_participants_global = None
            return
        except ValueError as error:
            fpath = error.args[0]
            if not self.first_load:
                self.label_error.configure(text="Neispravna datoteka.", text_color="red")
            return
        except Exception:
            logger.critical("Failed parcing participants!")
            self.label_error.configure(text="Nastupila pogreska!")
            raise

        if(cours_participants_global):
            self.label_4.configure(text=f"{path.basename(fpath)}")
            self.label_6.configure(text=f"{len(cours_participants_global)}")
            loaded_data[2] = True

    def BrowseAction(self):
        filename = filedialog.askopenfilename()
        self.entry_1.configure(state="normal")
        self.entry_1.delete(0, "end")
        self.entry_1.insert(0,filename)
        self.entry_1.configure(state="readonly")
        logger.info(f"Selected file: {filename}")


    def UploadAction(self):
        self.label_error.configure(text="")
        input_csv_file = self.entry_1.get()
        if(input_csv_file==""):
            logger.warning("Select a .csv file befor uploading.")
            self.label_error.configure(text="Nije zadana .csv datoteka.", text_color="red")
            return
        elif input_csv_file.endswith(".csv"):
            logger.info(f"{self.entry_1.get()}")
        else:
            logger.warning("Input file hase to be a .csv file.")
            self.label_error.configure(text="Zadana neispravna datoteka.", text_color="red")
            return
        
        #get path to old existing .csv file
        fpath: Path
        fpaths: list = glob.glob("data/*.csv")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} .csv files, there has to be only one!")
            self.label_error.configure(text="Neocekivana pogreska.", text_color="red")
            raise Exception
        elif(len(fpaths) == 0):
            logger.warning("No .csv file found!")
            self.label_error.configure(text="Neocekivana pogreska.", text_color="red")
        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                logger.info(f"Deleted {fpath}!")
            except Exception:
                logger.critical(f"Failed to delete {fpath}")
                self.label_error.configure(text="Neocekivana pogreska.", text_color="red")
                raise
        
        #get new selected .csv file
        fpath = Path(input_csv_file)
        try:
            copy(fpath, "data/")
            logger.info(f"Uploaded file: {fpath}!")
        except Exception:
            logger.critical(f"Failed to copy file: {fpath}!")
            self.label_error.configure(text="Neocekivana pogreska.", text_color="red")
            raise

        self.LoadParticipants()
        self.controller.scraper_frame.Reset_label()
    
class ScraperFrame(ctk.CTkFrame):
    def __init__(self, master, startdate:str, enddate:str):
        super().__init__(master)

        self.controller = master

        self.label_1 = ctk.CTkLabel(self, text="Raspored studenta", font=("Helvetica", 23))
        self.label_1.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 0), sticky="w")

        self.label_2 = ctk.CTkLabel(self, text="Preuzeti raspored u rasponu:")
        self.label_2.grid(row=1, column=0, padx=(10,0), pady=(10, 0), sticky="w")

        self.label_3 = ctk.CTkLabel(self, text="od - ")
        self.label_3.grid(row=1, column=1, padx=(5,0), pady=(10, 0), sticky="w")
        self.entry_1 = ctk.CTkEntry(self, placeholder_text="dd.mm.yyyy")
        self.entry_1.configure(state="normal")
        self.entry_1.grid(row=1, column=2, padx=(0, 5), pady=(10, 0), sticky="we")

        self.label_4 = ctk.CTkLabel(self, text="do - ")
        self.label_4.grid(row=1, column=3, padx=(5,0), pady=(10, 0), sticky="w")
        self.entry_2 = ctk.CTkEntry(self, placeholder_text="dd.mm.yyyy")
        self.entry_2.configure(state="normal")
        self.entry_2.grid(row=1, column=4, padx=(0, 5), pady=(10, 0), sticky="we")

        self.schedule_scrapper_button = ctk.CTkButton(self,width=60 , text="Preuzmi raspored", command=self.ScrapSchedule_thread)
        self.schedule_scrapper_button.grid(row=2, column=0, padx=(10,0), pady=10, sticky="")

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=2, column=1, columnspan=4, padx=(5,5), pady=10,sticky="wens")
        self.subframe.grid_columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self.subframe, text="Raspored studenta nije preuzet.")
        self.label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="")

        if not startdate=="":
            self.entry_1.insert(0,startdate)
        if not enddate=="":
            self.entry_2.insert(0,enddate)        

        self.Update_label()

    def Reset_label(self):
        loaded_data[3] = False
        self.label.configure(text="Raspored studenta nije preuzet.", text_color="white")
        if hasattr(self, "details_button"):
            self.details_button.grid_remove()

    def Update_label(self):
        global cours_participants_global, loaded_data

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        loaded_data[3] = False

        csvMissing = None
        csvEmpty = None

        try:
            if cours_participants_global:
                csvMissing, csvEmpty = schedule_scraper(cours_participants_global,False)
                loaded_data[3] = True
                #self.LoadedStatus(error="")
        except FileNotFoundError:
            logger.warning("Pleas scrape for new student schedule data.")
            return
        except ValueError:
            self.label.configure(text="Ucitani studenti nisu uskladeni sa preuzetim rasporedima za studente.", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
            return
        except Exception as error:
            Errors: list[Student] = error.args[0]
            logger.error(f"Errors with users: {*Errors,}")
            self.label.configure(text="Nastala neocekivana pogreska!", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
            return

        if csvMissing or csvEmpty:
            self.label.configure(text=f"Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}", text_color="white")
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text="Preuzmi detalje", command=lambda:self.ErrorDetails(csvMissing, csvEmpty))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
        elif cours_participants_global:
            self.LoadedStatus(error="")
    
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
            logger.critical("Error with creating Student_schedules_Error_detailes.xlsx")
            logger.exception()
        
        try:
            dest_dir = Path.home() / "Downloads"
            copy("data/Student_schedules_Error_detailes.xlsx", dest_dir)
            os.unlink("data/Student_schedules_Error_detailes.xlsx")
        except Exception:
            logger.exception("Error with downloading Student_schedules_Error_detailes.xlsx")
        
        self.details_button.configure(text="Preuzeto", text_color="green")
        self.details_button.after(1000, self.ResetDetailsButton)
    
    def ResetDetailsButton(self):
        self.details_button.configure(text="Preuzmi detalje", text_color="white")
        
    def LoadedStatus(self, error:str):
        if error=="":
            self.label.configure(text="Raspored studenta preuzet.", text_color="white")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        if error=="FileNotFoundError":
            self.label.configure(text="Pogreska! Nije zadana .csv datoteka sa studentima.", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        if error=="Exception":
            self.label.configure(text="Neocekivana pogreska!", text_color="red")
            if hasattr(self, "details_button"):
                self.details_button.grid_remove()
    
    def ScrapSchedule_thread(self):
        #reset variable cours_participants_global
        self.controller.participants_frame.LoadParticipants()

        startdate:str = self.entry_1.get()
        enddate:str = self.entry_2.get()
        if not self.ValidateDate(startdate):
            logger.warning(f"Entered invalid start date: {startdate}")
            self.label.configure(text="Pogreska sa prvim datumom.", text_color="red")
            return
        if not self.ValidateDate(enddate):
            logger.warning(f"Entered invalid end date: {enddate}")
            self.label.configure(text="Pogreska sa drugim datumom.", text_color="red")
            return
        logger.info(f"Entered valid dates: {startdate}, {enddate}")

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

        if not yyyy2 <= yyyy:
            pass
        elif not mm2 <= mm:
            pass
        elif not dd2 <= dd:
            pass
        else: 
            logger.warning("Start date is later than end date.")
            self.label.configure(text="Drugi datum je prije prvog.", text_color="red")
            return
        try:
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
                data["startdate"] = jsonstartdate
                data["enddate"] = jsonenddate
        except FileNotFoundError:
            data = {"cours":"","cours_number":"","startdate":jsonstartdate, "enddate":jsonenddate}
        
        json_object = json.dumps(data, indent=4)
        logger.info(f"Saving scraper dates: {jsonstartdate} - {jsonenddate}")
        with open("data/data.json", "w") as file:
            file.write(json_object)

        logger.info(f"Start date: {jsonstartdate}")
        logger.info(f"End date: {jsonenddate}")

        self.SetProgressBar()
        self.scrapper_progressbar.start()

        scrapper_thread = Thread(target=self.ScrapeSchedule, args=(startdate,enddate))
        scrapper_thread.start()

    def ScrapeSchedule(self, startdate:str, enddate:str):
        global cours_participants_global
        logger.info("Started thread for scraping schedule.")
        try:
            csvMissing, csvEmpty = schedule_scraper(cours_participants_global,True,startdate,enddate)
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.label.grid()
            loaded_data[3] = True
        except FileNotFoundError:
            logger.warning("Stoped schedule scraper.")
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.label.grid()
            self.LoadedStatus(error="FileNotFoundError")
            logger.info("Ending thread for scraping schedule.")
            return
        except Exception:
            logger.exception("Stoped schedule scraper.")
            self.scrapper_progressbar.stop()
            self.scrapper_progressbar.grid_remove()
            self.label.grid()
            self.LoadedStatus(error="Exception")
            logger.info("Ending thread for scraping schedule.")
            return

        
        if csvMissing or csvEmpty:
            self.label.configure(text=f"Potencijalne greske sa preuzetim rasporedima.\nBroj rasporeda koji nisu preuzeti: {len(csvMissing)}\nBroj praznih rasporeda: {len(csvEmpty)}", text_color="white")
            self.details_button = ctk.CTkButton(self.subframe,width=60 , text="Preuzmi detalje", command=lambda:self.ErrorDetails(csvMissing, csvEmpty))
            self.details_button.grid(row=1, column=0, padx=10, pady=10, sticky="")
        else:
            self.LoadedStatus(error="")
        
        logger.info("Ending thread for scraping schedule.")

    def SetProgressBar(self):
        self.label.grid_remove()
        if hasattr(self, "details_button"):
                self.details_button.grid_remove()
        self.scrapper_progressbar = ctk.CTkProgressBar(self.subframe, orientation="horizontal", mode="determinate", determinate_speed=2)
        self.scrapper_progressbar.grid(row=0, column=0, padx=5, pady=10, sticky="we")

    def ValidateDate(self, date:str)->bool:
        if not len(date.split("."))==3:
            return False
        dd, mm, yyyy = date.split(".")
        if not dd.isdigit() or not 0 < int(dd) <= 31:
            logger.warning(f"Error with dd: {dd}")
            return False
        elif not mm.isdigit() or not 0 < int(mm) <= 12:
            logger.warning(f"Error with mm: {mm}")
            return False
        elif not yyyy.isdigit() or not 2024 < int(yyyy) < 2100:
            logger.warning(f"Error with yyyy: {yyyy}")
            return False
        else:
            return True
        
class FillGroupsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        global continue_answer
        continue_answer = False
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.controller = master
        self.label_1 = ctk.CTkLabel(self, text="Ispuna grupa", font=("Helvetica", 23))
        self.label_1.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")

        global alfa_prio_label, alfa_prio_lvl
        self.alfa_prio_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.slider_event)
        self.alfa_prio_slider.configure(number_of_steps=100)
        self.alfa_prio_slider.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="")
        alfa_prio_lvl = int(self.alfa_prio_slider.get())
        self.alfa_prio_label = ctk.CTkLabel(self, text=f"Abecedni prioritet: {alfa_prio_lvl}")
        self.alfa_prio_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="")

        self.button_1 = ctk.CTkButton(self,width=60 , text="Pokreni", command=self.StartMainTask_thread)
        self.button_1.grid(row=3, column=0, padx=10, pady=10, sticky="")

        # self.main_task_progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", determinate_speed=2)
        # self.main_task_progressbar.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        # self.main_task_progressbar.grid_remove()

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=0, column=1, rowspan=4, padx=10, pady=10,sticky="wens")
        self.label_2 = ctk.CTkLabel(self.subframe, text="Postavite sve ulazne podatke za pokrenuti.")
        self.label_2.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)


    def slider_event(self,value):
        global alfa_prio_label, alfa_prio_lvl
        alfa_prio_lvl = int(value)
        self.alfa_prio_label.configure(text=f"Abecedni prioritet: {alfa_prio_lvl}")
    
    def CheckIfUserWantsToContinue(self)->bool:
        global total_places, cours_participants_global, continue_answer
        #Clear subframe
        for widget in self.subframe.winfo_children():
            widget.destroy()
        self.label_question = ctk.CTkLabel(self.subframe, text="Broj dostupnih mjesta je manji od broja studenta! Zelite li nastaviti?")
        self.label_question.grid(row=0,column=0, columnspan=2, padx=10, pady=(10,0))
        self.label_data = ctk.CTkLabel(self.subframe, text=f"Broj dostupnih mjesta: {total_places}; Broj studenta: {len(cours_participants_global)}")
        self.label_data.grid(row=1,column=0, columnspan=2, padx=10, pady=(10,0))

        self.button_yes = ctk.CTkButton(self.subframe, width=60 , text="DA", command=self.Yes)
        self.button_yes.grid(row=2,column=0, padx=10, pady=10)
        self.button_no = ctk.CTkButton(self.subframe, width=60 , text="NE", command=self.No)
        self.button_no.grid(row=2,column=1, padx=10, pady=10)

        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=0)
    
    def Yes(self):
        global continue_answer
        continue_answer = True
        self.StartMainTask_thread()
    
    def No(self):
        global continue_answer
        continue_answer = False
        #Clear subframe
        for widget in self.subframe.winfo_children():
            widget.destroy()
        self.label_question = ctk.CTkLabel(self.subframe, text="Zadatak prekinut")
        self.label_question.grid(row=0,column=0, columnspan=2, padx=10, pady=10)
        #self.subframe.grid_columnconfigure(0, weight=1)
        #self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)

    def MissingData(self):
        global loaded_data
        #Clear subframe
        for widget in self.subframe.winfo_children():
            widget.destroy()
        
        self.warning_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani potrebni podatci za pokretanje!", text_color="red")
        self.warning_label.grid(row=0,column=0, padx=10, pady=5, sticky="w")

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        row: int = 1
        if not loaded_data[0]:
            self.groups_not_loaded_label = ctk.CTkLabel(self.subframe, text="Grupe nisu ucitane!", text_color="red")
            self.groups_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1
        # if not loaded_data[1]:
        #     self.cours_not_loaded_label = ctk.CTkLabel(self.subframe, text="Naziv predmeta nije zadan!")
        #     self.cours_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
        #     row += 1
        if not loaded_data[2]:
            self.participants_not_loaded_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani studenti!", text_color="red")
            self.participants_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1
        if not loaded_data[3]:
            self.student_schedule_not_loaded_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani rasporedi studenta!", text_color="red")
            self.student_schedule_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1

    def StartMainTask_thread(self):
        self.button_1.grid_remove()
        self.main_task_progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", determinate_speed=2)
        
        global total_places, cours_participants_global, continue_answer, loaded_data

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        if not loaded_data[0] or not loaded_data[2] or not loaded_data[3]:
            self.MissingData()
            self.button_1.grid()
            self.main_task_progressbar.destroy()
            return

        cours_name_entry: ctk.CTkEntry = self.controller.cours_frame.cours_name_entry
        cours_name = cours_name_entry.get()

        cours_number_entry: ctk.CTkEntry = self.controller.cours_frame.cours_number_entry
        cours_number = cours_number_entry.get()

        with open("data/data.json", "r") as file:
            data:dict[str:str] = json.load(file)

        data["cours"] = cours_name
        data["cours_number"] = cours_number
        json_object = json.dumps(data, indent=4)

        logger.info(f"Saving cours data: {cours_name} - {cours_number}")

        with open("data/data.json", "w") as file:
            file.write(json_object)

        #Clear subframe and set progress bar
        if total_places < len(cours_participants_global) and not continue_answer:
            self.CheckIfUserWantsToContinue()
            self.button_1.grid()
            self.main_task_progressbar.destroy()
            return
        continue_answer = False
        for widget in self.subframe.winfo_children():
            widget.destroy()
        self.main_task_progressbar.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.main_task_progressbar.start()
        #self.button_1.configure(state="disabled")
        
        scrapper_thread = Thread(target=self.FillGroups_thread)
        scrapper_thread.start()
    
    def FillGroups_thread(self):
        global alfa_prio_lvl, cours_participants_global
        weight_errors:list[Student] = []
        fill_errors:list[Student] = []
        running: bool = True
        counter: int = 0
        group: Group
        groups_on_day: list[Group]

        cours_participants_local: dict[str, Student]
        groups_local: dict[str, list[Group]]

        try:
            while running and counter<=100:
                logger.info(f"Now running attempt {counter}.")
                #Get cours participants
                try:
                    logger.info("Starting participants parser!")   
                    cours_participants_local, _ = pars_cours_participants()
                    cours_participants_copy = cours_participants_local.copy()
                    logger.info(f"Found {len(cours_participants_local)} students in participants file.")
                except TypeError:
                    raise logger.exception("Failed parsing participants!")
                
                #Get lab group schedule
                try:
                    logger.info("Starting schedule parser!")
                    groups_local, _ = pars_schedule_file()
                    numofgroups:int = 0
                    day: str
                    for day in groups_local:
                        numofgroups += len(groups_local[day])
                        logger.info(f"Found {len(groups_local[day])} groups for {day}")
                    logger.info(f"Found {numofgroups} groups in total!")
                except Exception:
                    logger.error('Failed parsing schedule!')
                    raise

                #Get schedule for every student
                try:
                    schedule_scraper(cours_participants_local, False)
                except Exception:
                    logger.error("Error when scraping schedule!")
                    raise
                
                #Generate starting weights, weight_errors are students that cant join any group at all
                try:
                    weight_errors = weight_generator(cours_participants_local, groups_local, alfa_prio_lvl)
                except Exception:
                    logger.error("Error generating starting weights!")
                    raise
                
                success, fill_errors = fill_groups(cours_participants_local, groups_local, 1)
                if success:
                    running = False
                    logger.info("Successfully filled out all groups with no students remaining!")
                    for groups_on_day in groups_local.values():
                        for group in groups_on_day:
                            logger.info(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
                            logger.info("------------------------------------------------------------------")
                else:
                    counter += 1
            cours_participants_global = cours_participants_copy
            self.CreateExcelWorkbook()
            self.LoadStatus(success, weight_errors, fill_errors)
            self.main_task_progressbar.stop()
            self.main_task_progressbar.destroy()
            self.button_1.grid()
        except Exception:
            logger.error("Error filling groups!")
            self.button_1.grid()
            self.main_task_progressbar.destroy()
            raise
    
    def LoadStatus(self,success:bool, weight_errors:list[Student], fill_errors:list[Student]):
        for widget in self.subframe.winfo_children():
            widget.destroy()
        if success:
            self.label_2 = ctk.CTkLabel(self.subframe, text="Grupe popunjene.",font=("Helvetica", 18))
        else:
            self.label_2 = ctk.CTkLabel(self.subframe, text="Pogreska pri punjenju grupa.",font=("Helvetica", 18), text_color="red")
        self.label_2.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

        if weight_errors or fill_errors:
            self.errorsubframe = ctk.CTkFrame(self.subframe)
            self.errorsubframe.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
            self.label_3 = ctk.CTkLabel(self.errorsubframe, text=f"Broj studenta kojima ne odgovara niti jedna grupa: {len(weight_errors)}", text_color="red")
            self.label_3.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")
            self.label_4 = ctk.CTkLabel(self.errorsubframe, text=f"Broj studenta koji nisu uspjesno svrstani u grupu: {len(fill_errors)}", text_color="red")
            self.label_4.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="w")
            self.label_5 = ctk.CTkLabel(self.errorsubframe, text="Preuzmi datoteku sa detaljima:")
            self.label_5.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="w")
            self.button_3 = ctk.CTkButton(self.errorsubframe, width=60, text="Preuzmi", command=lambda:self.CopyErrorWeightsToDownloads(weight_errors,fill_errors))
            self.button_3.grid(row=2, column=0, columnspan=2, padx=(150,20), pady=(0, 5), sticky="e")
        # else:
        #     self.label_3 = ctk.CTkLabel(self.subframe, text=f"Broj studenti kojima ne odgovara niti jedna grupa: N/A")
        #     self.label_3.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.label_6 = ctk.CTkLabel(self.subframe, text="Excel datoteka sa popunjenim grupama:")
        self.label_6.grid(row=2, column=0, padx=(20,0), pady=10, sticky="w")
        self.button_2 = ctk.CTkButton(self.subframe, width=60, text="Preuzmi", command=self.CopyFilledGroupsToDownloads)
        self.button_2.grid(row=2, column=0, columnspan=2, padx=(120,0), pady=10, sticky="")

        self.subframe.grid_columnconfigure(0, weight=1)
        #self.subframe.grid_columnconfigure(1, weight=0)
        self.subframe.grid_rowconfigure(0, weight=0)

    def ResetDownloadButton_2(self):
        self.button_2.configure(text="Preuzmi", text_color="white")
    def ResetDownloadButton_3(self):
        self.button_3.configure(text="Preuzmi", text_color="white")

    def CopyErrorWeightsToDownloads(self,weight_errors:list[Student],fill_errors:list[Student]):
        try:
            workbook = xlsxwriter.Workbook("data/Error_detailes.xlsx")
            worksheet = workbook.add_worksheet()
            worksheet.write("A1", f"Broj studenta kojima ne odgovara niti jedna grupa: {len(weight_errors)}", workbook.add_format({"border":2, "bottom":1}))
            worksheet.write("A2", f"Broj studenta koji nisu uspjesno svrstani u grupu: {len(fill_errors)}", workbook.add_format({"border":2, "top":1}))
            worksheet.write("A4", "Studenti")
            worksheet.write("B4", "Dostupne grupe")
            worksheet.write("C4", "Nesvrstani studenti")
            worksheet.write("D4", "Dostupne grupe")
            worksheet.write("E4", "Studenti bez grupe")

            f1=workbook.add_format({"border":1, "left":5, "right":5})   #Thick left and right
            f2=workbook.add_format({"border":1, "right":5})             #Thick right
            f3=workbook.add_format({"border":1, "left":5})              #Thick left

            row: int = 5
            for student in cours_participants_global.values():
                worksheet.write(f"A{row}", f"{student}", f3)
                if hasattr(student, "groups"):
                    worksheet.write(f"B{row}", f"{*student.groups,}", f2)
                else:
                    worksheet.write(f"B{row}", "Bez grupe")
                row += 1
            
            row: int = 5
            for student in fill_errors:
                worksheet.write(f"C{row}", f"{student}", f3)
                if hasattr(student, "groups"):
                    worksheet.write(f"D{row}", f"{*student.groups,}", f2)
                else:
                    worksheet.write(f"D{row}", "Bez grupe")
                row += 1
            
            row: int = 5
            for student in weight_errors:
                worksheet.write(f"E{row}", f"{student}", f1)
                row += 1
            
            workbook.close()
        except Exception:
            logger.critical("Error with creating Error_detailes.xlsx")
            logger.exception()

        try:
            dest_dir = Path.home() / "Downloads"
            copy("data/Error_detailes.xlsx", dest_dir)
            os.unlink("data/Error_detailes.xlsx")
        except Exception:
            logger.exception("Error with downloading Error_detailes.xlsx")
        
        self.button_3.configure(text="Preuzeto", text_color="green")
        self.button_3.after(1000, self.ResetDownloadButton_3)

    def CopyFilledGroupsToDownloads(self):
        try:
            cours_name_entry: ctk.CTkEntry = self.controller.cours_frame.cours_name_entry
            cours_name = cours_name_entry.get()
            if cours_name=="":
                cours_name = "predmet"

            cours_number_entry: ctk.CTkEntry = self.controller.cours_frame.cours_number_entry
            cours_number = cours_number_entry.get()
            if cours_number=="":
                cours_number = "smjer"

            srcfile = "data/Filled_Groups.xlsx"
            dest_dir = Path.home() / "Downloads"
            copy(srcfile, dest_dir)
            new_name = f"{dest_dir}/{cours_name}-{cours_number}-Popunjene_Grupe.xlsx"
            move(f"{dest_dir}/Filled_Groups.xlsx", new_name)
            #os.unlink("data/Filled_Groups.xlsx")
        except Exception:
            logger.critical("Error when moving excel result file to downloads.")
        self.button_2.configure(text="Preuzeto", text_color="green")
        self.button_2.after(1000, self.ResetDownloadButton_2)
    
    def CreateExcelWorkbook(self):
        global cours_participants_global
        workbook = xlsxwriter.Workbook("data/Filled_Groups.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write("A1", "Prezime")
        worksheet.write("B1", "Ime")
        worksheet.write("C1", "Email")
        worksheet.write("D1", "ID broj")
        worksheet.write("E1", "Korisničko ime")
        worksheet.write("F1", "Grupa")

        row: int = 2
        for student in cours_participants_global.values():
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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        Path("data").mkdir(exist_ok=True)

        self.title("Lab generator")
        #self.geometry("1070x700")
        self.resizable(False, False)
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        global loaded_data
        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        loaded_data = [False, False, False, False]

        self.schedule_frame = GroupsFrame(self)
        self.schedule_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nswe")

        self.right_frame = RightFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)

def main():
    app = App()    
    try:
        app.mainloop()
    except Exception:
        logger.exception("Exiting app!")
        exit()

if __name__ == "__main__":
    main()