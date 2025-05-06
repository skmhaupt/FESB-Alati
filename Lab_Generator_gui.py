from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.classes import CustomFormatter
from labgenpackage.classes import Student
from labgenpackage.classes import Group
from customtkinter import filedialog
from pathlib import Path
from shutil import copy
from os import path
import customtkinter as ctk
import logging.config
import logging
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
        }
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["stdout"]}
    }
}
logging.config.dictConfig(config=logging_config)
ch = logging.getHandlerByName("stdout")
ch.setFormatter(CustomFormatter())
logger = logging.getLogger("my_app")


class GroupsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)

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
        self.button_2.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="")
        
        self.label_num_of_groups = ctk.CTkLabel(self, text="Broj grupa nepoznat")
        self.label_num_of_groups.grid(row=4, column=0, padx=(10,0), pady=(5, 0), sticky="we")
        self.label_num_of_places = ctk.CTkLabel(self, text="Broj dostupnih mjesta nije poznat.")
        self.label_num_of_places.grid(row=4, column=1, columnspan=2, padx=(0,5), pady=(5, 0), sticky="we")

        self.subframe = ctk.CTkScrollableFrame(self)
        self.subframe.grid(row=5, column=0, columnspan=3, padx=10, pady=10,sticky="wens")
        self.label_3 = ctk.CTkLabel(self.subframe, text="Grupe nisu ucitane.")
        self.label_3.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="we")

        self.LoadGroups()
    
    def LoadGroups(self)->str:
        global groups
        try:
            groups, fpath = pars_schedule_file()
        except Exception:
            logger.error("Failed parcing participants!")
            raise

        for widget in self.subframe.winfo_children():
            widget.destroy()  # deleting widget

        row:int = 2
        total_places:int = 0
        group:Group
        for groups_in_day in groups.values():
            for group in groups_in_day:
                self.AddGrouplabel(row,group)
                total_places+=group.group_size
                row+=1
        logger.info(f"Found {row-1} groups. With {total_places} places in total.")
        
        self.label_num_of_groups.configure(text=f"Broj grupa: {row-2}")
        self.label_num_of_places.configure(text=f"Broj dostupnih mjesat: {total_places}")

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
            return
        elif input_txt_file.endswith(".txt"):
            logger.info(f"{self.entry_1.get()}")
        else:
            logger.warning("Input file hase to be a .txt file.")
            return
        
        #get path to old existing .txt file
        fpath: Path
        fpaths: list = glob.glob("data/*.txt")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} .txt files, there has to be only one!")
            raise Exception
        elif(len(fpaths) == 0):
            logger.warning("No .txt file found!")
        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                logger.info(f"Deleted {fpath}!")
            except Exception:
                logger.critical(f"Failed to delete {fpath}")
                raise
        
        #get new selected .txt file
        fpath = Path(input_txt_file)
        try:
            copy(fpath, "data/")
            logger.info(f"Uploaded file: {fpath}!")
        except Exception:
            logger.critical(f"Failed to copy file: {fpath}!")
            raise

        self.LoadGroups()

#Contains the right side of the UI: CoursFrame, ParticipantsFrame, ...
class RightFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.cours_frame = CoursFrame(self)
        self.cours_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")

        self.participants_frame = ParticipantsFrame(self)
        self.participants_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.scraper_frame = ScraperFrame(self)
        self.scraper_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.fill_groups_frame = FillGroupsFrame(self)
        self.fill_groups_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


#First segment of the right side of the UI. Hold the section for cours data
class CoursFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label_1 = ctk.CTkLabel(self, text="Predmet:")
        self.label_1.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="w")
        self.entry_1 = ctk.CTkEntry(self, placeholder_text="npr: PDS, SDOS, itd.")
        self.entry_1.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="e")

        self.label_2 = ctk.CTkLabel(self, text="Smjer:")
        self.label_2.grid(row=0, column=2, padx=(10, 5), pady=(10, 10), sticky="w")
        self.entry_2 = ctk.CTkEntry(self, placeholder_text="npr: 112, 222 itd.")
        self.entry_2.grid(row=0, column=3, padx=(0, 10), pady=(10, 10), sticky="e")

class ParticipantsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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

        self.LoadParticipants()
        

    def LoadParticipants(self)->str:
        global cours_participants
        try:
            cours_participants, fpath = pars_cours_participants()
        except Exception:
            logger.error("Failed parcing participants!")
            raise

        logger.info(f"Found {len(cours_participants)} students!")
        if(cours_participants):
            self.label_4.configure(text=f"{path.basename(fpath)}")
            self.label_6.configure(text=f"{len(cours_participants)}")

    def BrowseAction(self):
        filename = filedialog.askopenfilename()
        self.entry_1.configure(state="normal")
        self.entry_1.delete(0, "end")
        self.entry_1.insert(0,filename)
        self.entry_1.configure(state="readonly")
        logger.info(f"Selected file: {filename}")


    def UploadAction(self):
        input_csv_file = self.entry_1.get()
        if(input_csv_file==""):
            logger.warning("Select a .csv file befor uploading.")
            return
        elif input_csv_file.endswith(".csv"):
            logger.info(f"{self.entry_1.get()}")
        else:
            logger.warning("Input file hase to be a .csv file.")
            return
        
        #get path to old existing .csv file
        fpath: Path
        fpaths: list = glob.glob("data/*.csv")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} .csv files, there has to be only one!")
            raise Exception
        elif(len(fpaths) == 0):
            logger.warning("No .csv file found!")
        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                logger.info(f"Deleted {fpath}!")
            except Exception:
                logger.critical(f"Failed to delete {fpath}")
                raise
        
        #get new selected .csv file
        fpath = Path(input_csv_file)
        try:
            copy(fpath, "data/")
            logger.info(f"Uploaded file: {fpath}!")
        except Exception:
            logger.critical(f"Failed to copy file: {fpath}!")
            raise

        self.LoadParticipants()
    
class ScraperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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

        self.button_1 = ctk.CTkButton(self,width=60 , text="Preuzmi raspored", command=self.ScrapeSchedule)
        self.button_1.grid(row=2, column=0, padx=(10,0), pady=10, sticky="w")

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=2, column=1, columnspan=4, padx=(5,5), pady=10,sticky="wens")
        self.label_3 = ctk.CTkLabel(self.subframe, text="Raspored studenta nije preuzet.")
        self.label_3.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="we")

        global cours_participants
        try:
            schedule_scraper(cours_participants,False)
        except FileNotFoundError:
            logger.warning("Pleas load a new cours participants .csv file or scrape for a new student schedule data.")
            return
        
        self.LoadedStatus()
        
    def LoadedStatus(self):
        #len([name for name in os.listdir('.') if os.path.isfile(name)])

        for widget in self.subframe.winfo_children():
            widget.destroy()

        self.label = ctk.CTkLabel(self.subframe, text="Raspored studenta preuzet.")
        self.label.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="we")
    
    def ScrapeSchedule(self):
        startdate:str = self.entry_1.get()
        enddate:str = self.entry_2.get()
        if not self.ValidateDate(startdate):
            logger.warning(f"Entered invalid start date: {startdate}")
            return
        if not self.ValidateDate(enddate):
            logger.warning(f"Entered invalid end date: {enddate}")
            return
        logger.info(f"Entered valid dates: {startdate}, {enddate}")

        dd,mm,yyyy=startdate.split(".")
        dd=int(dd)
        mm=int(mm)
        yyyy=int(yyyy)
        startdate = f"{dd:02}-{mm:02}-{yyyy:04}"

        dd2,mm2,yyyy2=enddate.split(".")
        dd2=int(dd2)
        mm2=int(mm2)
        yyyy2=int(yyyy2)
        enddate = f"{dd2:02}-{mm2:02}-{yyyy2:04}"

        if not yyyy2 <= yyyy:
            pass
        elif not mm2 <= mm:
            pass
        elif not dd2 <= dd:
            pass
        else: 
            logger.warning("Start date is later than end date.")
            return

        
        logger.info(f"Start date: {startdate}")
        logger.info(f"End date: {enddate}")
        global cours_participants
        # for stutdent in cours_participants.values():
        #     print(stutdent)
        schedule_scraper(cours_participants,True,startdate,enddate)

        self.LoadedStatus()

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

        self.grid_columnconfigure(0, weight=1)

        self.label_1 = ctk.CTkLabel(self, text="Ispuna grupa", font=("Helvetica", 23))
        self.label_1.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")

        self.button_1 = ctk.CTkButton(self,width=60 , text="Pokreni", command=self.StartMainTask)
        self.button_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="")

        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=2, column=0, padx=10, pady=10,sticky="wens")
        self.label_2 = ctk.CTkLabel(self.subframe, text="Raspored studenta nije preuzet.")
        self.label_2.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="we")

    def StartMainTask():
        global cours_participants
        global groups
        pass
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lab generator")
        self.geometry("1070x600")
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
    cours_participants: dict[str, Student] = {}
    groups: dict[str, list:Group] = {}
    main()