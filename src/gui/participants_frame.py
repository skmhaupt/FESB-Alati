from labgenpackage.participants_parser import pars_cours_participants
from customtkinter import filedialog
from pathlib import Path
from shutil import copy
from os import path

import gui.settings as settings
import customtkinter as ctk
import logging, glob

class ParticipantsFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        from gui.right_frame import RightFrame
        super().__init__(master)

        self.controller: RightFrame = master
        self.logger = logger

        self.grid_columnconfigure(1, weight=1)

        self.section_title_label = ctk.CTkLabel(self, text="Sudionici", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")

        self.entry_label = ctk.CTkLabel(self, text="Ulazna datoteka:")
        self.entry_label.grid(row=1, column=0, padx=(10, 5), pady=(10, 0), sticky="w")

        self.csv_file_entry = ctk.CTkEntry(self, placeholder_text=".csv datoteka")   # this widget will containe the path to the .csv file
        self.csv_file_entry.configure(state="readonly")
        self.csv_file_entry.grid(row=1, column=1, padx=(0, 5), pady=(10, 0), sticky="we")
        
        self.browse_button = ctk.CTkButton(self,width=60 , text="Pretrazi", command=self.BrowseAction)  # button to get path to .csv file
        self.browse_button.grid(row=1, column=2, padx=(0, 10), pady=(10, 0), sticky="e")

        self.upload_button = ctk.CTkButton(self,width=125 , text="Ucitaj datoteku", command=self.UploadAction)  # button to load the selected .csv file
        self.upload_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="")

        self.label_error = ctk.CTkLabel(self, text="", text_color="red")    # label for all errors
        self.label_error.grid(row=2, column=1, columnspan=2, padx=10, pady=(10, 0), sticky="w")

        # subframe that will display loaded data
        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=3, column=0, columnspan=3, padx=10, pady=10,sticky="")

        self.label_1 = ctk.CTkLabel(self.subframe, text="Ucitana datoteka:")
        self.label_1.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
        self.loaded_csv_file_name_label = ctk.CTkLabel(self.subframe, text="Trenutno nije ucitana .csv datoteka!")
        self.loaded_csv_file_name_label.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="w")
        
        self.label_2 = ctk.CTkLabel(self.subframe, text="Broj ucitanih studenta:")
        self.label_2.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="w")
        self.num_of_students_label = ctk.CTkLabel(self.subframe, text="Trenutno nije ucitana .csv datoteka!")
        self.num_of_students_label.grid(row=1, column=1, padx=(10, 10), pady=(0, 10), sticky="w")

        # load data from old session on startup
        self.first_load = True
        self.LoadParticipants()
        self.first_load = False

    # get path to .csv file from user
    def BrowseAction(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.csv_file_entry.configure(state="normal")
        self.csv_file_entry.delete(0, "end")
        self.csv_file_entry.insert(0,filename)
        self.csv_file_entry.configure(state="readonly")
        self.logger.info(f"Selected file: {filename}")

    # 'UploadAction' runs from 'upload_button'. Sets 'loaded_data[2]' to False in order to block the main section from starting.
    # (loaded_data[2]: bool = flag for participants_loaded)
    # Makes preparations for 'LoadParticipants'
    def UploadAction(self):
        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        settings.loaded_data[2] = False     # this will probably always already be false at this point

        if settings.working:
            self.logger.warning("Already runing another section! Cant upload new groups.")
            self.label_error.configure(text="Vec je pokrenuta druga sekcija!")
            return
        else: settings.working = True   # block other sections from starting

        self.label_error.configure(text="")     # reset error label

        # get path to input .csv file and check for errors
        input_csv_file = self.csv_file_entry.get()
        if(input_csv_file==""):
            self.logger.warning("Select a .csv file befor uploading.")
            self.label_error.configure(text="Nije zadana .csv datoteka.")
            settings.working = False
            return
        elif input_csv_file.endswith(".csv"):
            self.logger.info(f"{self.csv_file_entry.get()}")
        else:
            self.logger.warning("Input file hase to be a .csv file.")
            self.label_error.configure(text="Zadana neispravna datoteka.")
            settings.working = False
            return
        
        #get path to old existing .csv file and delete it
        fpath: Path
        fpaths: list = glob.glob("data/*.csv")
        if(len(fpaths) > 1):    # this is unexpected and schould ony happen if there is a bug
            self.logger.critical(f"Found {len(fpaths)} .csv files, there has to be only one!")
            
            try:
                for pathstr in fpaths:
                    self.logger.critical(f"Erasing {pathstr}")
                    delpath = Path(pathstr)
                    delpath.unlink()

            except Exception:
                self.logger.critical(f"Failed to delete old txt file {pathstr}")
                self.label_error.configure(text="Neocekivana pogreska.")
                settings.working = False
                return
            
        elif(len(fpaths) == 0):
            self.logger.warning("No .csv file found!")

        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                self.logger.info(f"Deleted old .csv file {fpath}!")
            except Exception:
                self.logger.critical(f"Failed to delete old .csv file {fpath}")
                self.label_error.configure(text="Neocekivana pogreska.")
                settings.working = False
                return
        
        #get new selected .csv file
        fpath = Path(input_csv_file)
        try:
            copy(fpath, "data/")
            self.logger.info(f"Uploaded file: {fpath}!")
        except Exception:
            self.logger.critical(f"Failed to copy file: {fpath}!")
            self.label_error.configure(text="Neocekivana pogreska.")
            settings.working = False
            return

        self.LoadParticipants()
        self.controller.scraper_frame.Reset_label()
        settings.working = False

    # 'LoadParticipants' runs on sturtup and when loading new .csv file after the 'UploadAction' function. It runs the 'pars_cours_participants'
    # function for as a test and displays sucesfuly loaded students and errors. The main section of the program will not run until
    # this section sets loaded_data[2] to True. (loaded_data[2]: bool = flag for participants_loaded)
    def LoadParticipants(self):
        # loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        settings.loaded_data[2] = False     # this will probably always already be false at this point

        try:
            settings.cours_participants_global, fpath = pars_cours_participants()
            self.logger.info(f"Found {len(settings.cours_participants_global)} students!")
            self.label_error.configure(text="")
        except FileNotFoundError:   # this should never occur as it has already been verified in 'UploadAction'
            self.logger.critical("File not founde. Returning from LoadParticipants()!")
            settings.cours_participants_global = None
            return
        except ValueError as error:
            fpath = error.args[0]
            if not self.first_load:
                self.label_error.configure(text="Neispravna datoteka.")
            return
        except Exception:
            self.logger.critical("Failed parcing participants!")
            self.label_error.configure(text="Nastupila pogreska!")
            return

        # display summary of loaded data
        if(settings.cours_participants_global):
            self.loaded_csv_file_name_label.configure(text=f"{path.basename(fpath)}")
            self.num_of_students_label.configure(text=f"{len(settings.cours_participants_global)}")
            settings.loaded_data[2] = True      # set flag for participants_loaded, this is here because 'UploadAction' is not called on startup