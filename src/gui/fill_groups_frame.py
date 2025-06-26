from excel_functions.fill_groups_results import GenErrorDetailsWorkbook, GenResultsWorkbook
from labgenpackage.participants_parser import pars_cours_participants
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.fill_groups import fill_groups
from labgenpackage.classes import Student, Group
from shutil import copy, move
from threading import Thread
from pathlib import Path

import customtkinter as ctk
import gui.settings as settings
import logging, xlsxwriter, os, json

class FillGroupsFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)

        self.controller = master    # in case ctk widgets from other sections have to be accessed
        self.logger = logger

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.controller = master
        self.section_title_label = ctk.CTkLabel(self, text="Ispuna grupa", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="nw")

        #global alfa_prio_label, alfa_prio_lvl
        self.alfa_prio_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.slider_event)
        self.alfa_prio_slider.configure(number_of_steps=20)
        self.alfa_prio_slider.set(0)
        self.alfa_prio_slider.grid(row=1, column=0, padx=10, pady=(30, 0), sticky="s")
        settings.alfa_prio_lvl = int(self.alfa_prio_slider.get())
        self.alfa_prio_label = ctk.CTkLabel(self, text=f"Abecedni prioritet: {settings.alfa_prio_lvl}")
        self.alfa_prio_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="n")

        self.fill_groups_button = ctk.CTkButton(self,width=60 , text="Pokreni", command=self.FillGroups_setup)  # button to start main task setup
        self.fill_groups_button.grid(row=3, column=0, padx=10, pady=10, sticky="n")

        # subframe for satus display
        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=0, column=1, rowspan=5, padx=10, pady=10,sticky="wens")
        self.default_status_label = ctk.CTkLabel(self.subframe, text="Postavite sve ulazne podatke za pokrenuti.")
        self.default_status_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)

    # sync slider label and slider value
    def slider_event(self,value):
        #global alfa_prio_label, alfa_prio_lvl
        settings.alfa_prio_lvl = int(value)
        self.alfa_prio_label.configure(text=f"Abecedni prioritet: {settings.alfa_prio_lvl}")
    
    # ask user if he wants to run the main section even if the number of places is smaller than the number of students
    def CheckIfUserWantsToContinue(self)->bool:
        for widget in self.subframe.winfo_children():   # deleting all old widgets in subframe
            widget.destroy()

        self.label_question = ctk.CTkLabel(self.subframe, text="Broj dostupnih mjesta je manji od broja studenta! Zelite li nastaviti?")
        self.label_question.grid(row=0,column=0, columnspan=2, padx=10, pady=(10,0),sticky="s")
        self.label_data = ctk.CTkLabel(self.subframe, text=f"Broj dostupnih mjesta: {settings.total_places}; Broj studenta: {len(settings.cours_participants_global)}")
        self.label_data.grid(row=1,column=0, columnspan=2, padx=10, pady=(10,0))

        self.button_yes = ctk.CTkButton(self.subframe, width=60 , text="DA", command=self.Yes)
        self.button_yes.grid(row=2,column=0, padx=10, pady=10,sticky="n")
        self.button_no = ctk.CTkButton(self.subframe, width=60 , text="NE", command=self.No)
        self.button_no.grid(row=2,column=1, padx=10, pady=10,sticky="n")

        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)
        self.subframe.grid_rowconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(2, weight=1)
    
    # user wants to run the main section
    def Yes(self):
        settings.continue_answer = True
        self.FillGroups_setup()
    
    # user doesnt wants to run the main section
    def No(self):
        settings.continue_answer = False

        for widget in self.subframe.winfo_children():   # deleting all old widgets in subframe
            widget.destroy()

        self.label_question = ctk.CTkLabel(self.subframe, text="Zadatak prekinut")
        self.label_question.grid(row=0,column=0, columnspan=2, padx=10, pady=10)
        #self.subframe.grid_columnconfigure(0, weight=1)
        #self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)

    # display error msg in subframe if missing input data
    def MissingData(self):
        for widget in self.subframe.winfo_children():   # deleting all old widgets in subframe
            widget.destroy()
        
        self.warning_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani potrebni podatci za pokretanje!", text_color="red")
        self.warning_label.grid(row=0,column=0, padx=10, pady=5, sticky="w")

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        row: int = 1
        if not settings.loaded_data[0]:     # missing group data
            self.groups_not_loaded_label = ctk.CTkLabel(self.subframe, text="Grupe nisu ucitane!", text_color="red")
            self.groups_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1
        # if not settings.loaded_data[1]:
        #     self.cours_not_loaded_label = ctk.CTkLabel(self.subframe, text="Naziv predmeta nije zadan!")
        #     self.cours_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
        #     row += 1
        if not settings.loaded_data[2]:     # missing student data
            self.participants_not_loaded_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani studenti!", text_color="red")
            self.participants_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1
        if not settings.loaded_data[3]:     # missing student schedule data
            self.student_schedule_not_loaded_label = ctk.CTkLabel(self.subframe, text="Nisu ucitani rasporedi studenta!", text_color="red")
            self.student_schedule_not_loaded_label.grid(row=row,column=0, padx=10, pady=0)
            row += 1

    # Is called on 'fill_groups_button' press. Makes all needed preparations before running main task thread
    def FillGroups_setup(self):
        self.fill_groups_button.grid_remove()

        if settings.working:    # only one section can run at a time. This prevents unpredictable errors. - temporary fix
            self.logger.warning("Already runing another section! Cant upload new groups.")

            for widget in self.subframe.winfo_children():   # deleting all old widgets in subframe
                widget.destroy()
            
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Vec je pokrenuta druga sekcija.\nSacekajte dok ne zavrsi sa izvodenjem", text_color="red")
            self.warning_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
            self.fill_groups_button.grid()
            return
        
        else: settings.working = True   # block other sections from starting
        

        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        if not settings.loaded_data[0] or not settings.loaded_data[2] or not settings.loaded_data[3]:
            self.MissingData()
            settings.working = False
            self.fill_groups_button.grid()
            return
        
        # check if sufficient space is available in loaded groups
        if settings.total_places < len(settings.cours_participants_global) and not settings.continue_answer:
            self.CheckIfUserWantsToContinue()
            settings.working = False
            self.fill_groups_button.grid()
            return
        settings.continue_answer = False

        # get cours data and save it to data.json
        cours_name_entry: ctk.CTkEntry = self.controller.cours_frame.cours_name_entry
        cours_name = cours_name_entry.get()
        cours_number_entry: ctk.CTkEntry = self.controller.cours_frame.cours_number_entry
        cours_number = cours_number_entry.get()
        with open("data/data.json", "r") as file:
            data:dict[str:str] = json.load(file)
        data["cours"] = cours_name
        data["cours_number"] = cours_number
        json_object = json.dumps(data, indent=4)
        self.logger.info(f"Saving cours data: {cours_name} - {cours_number}")
        with open("data/data.json", "w") as file:
            file.write(json_object)

        #Clear subframe and set progress bar
        for widget in self.subframe.winfo_children():   # deleting all old widgets in subframe
            widget.destroy()

        self.main_task_progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", determinate_speed=2)
        self.main_task_progressbar.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.main_task_progressbar.start()
        
        scrapper_thread = Thread(target=self.FillGroups_thread)
        scrapper_thread.start()
    
    def FillGroups_thread(self):
        success = False
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
                self.logger.info(f"Now running attempt {counter}.")
                #Get cours participants
                try:
                    self.logger.info("Starting participants parser!")   
                    cours_participants_local, _ = pars_cours_participants()
                    cours_participants_copy = cours_participants_local.copy()   # a shallow copy is needed to preserve the results as data is poped from the dict
                    self.logger.info(f"Found {len(cours_participants_local)} students in participants file.")
                except TypeError:
                    raise self.logger.exception("Failed parsing participants!")
                
                #Get lab group schedule
                try:
                    self.logger.info("Starting schedule parser!")
                    groups_local, _, _ = pars_schedule_file()
                    numofgroups:int = 0
                    day: str
                    for day in groups_local:
                        numofgroups += len(groups_local[day])
                        self.logger.info(f"Found {len(groups_local[day])} groups for {day}")
                    self.logger.info(f"Found {numofgroups} groups in total!")
                except Exception:
                    self.logger.error('Failed parsing schedule!')
                    raise

                #Get schedule for every student
                try:
                    schedule_scraper(cours_participants_local, False)
                except Exception:
                    self.logger.error("Error when scraping schedule!")
                    raise
                
                #Generate starting weights; weight_errors are students that cant join any group at all
                try:
                    weight_errors = weight_generator(cours_participants_local, groups_local, settings.alfa_prio_lvl)
                except Exception:
                    self.logger.error("Error generating starting weights!")
                    raise
                
                # fill groups with students
                success, fill_errors = fill_groups(cours_participants_local, groups_local, 1)
                if success:
                    running = False
                    self.logger.info("Successfully filled out all groups with no students remaining!")
                    for groups_on_day in groups_local.values():
                        for group in groups_on_day:
                            self.logger.info(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
                            self.logger.info("------------------------------------------------------------------")
                else:
                    counter += 1
            
            # display results of fill_groups
            settings.cours_participants_result = cours_participants_copy
            GenResultsWorkbook()
            #self.CreateExcelWorkbook()
            self.LoadStatus(success, weight_errors, fill_errors)
            self.main_task_progressbar.stop()
            self.main_task_progressbar.destroy()
            self.fill_groups_button.grid()
            settings.working = False
        except Exception:
            self.logger.error("Error filling groups!")
            self.LoadStatus(success, weight_errors, fill_errors)
            self.fill_groups_button.grid()
            self.main_task_progressbar.destroy()
            settings.working = False
            return
    
    def LoadStatus(self,success:bool, weight_errors:list[Student], fill_errors:list[Student]):
        for widget in self.subframe.winfo_children():
            widget.destroy()

        if success:
            self.status_header_label = ctk.CTkLabel(self.subframe, text="Grupe popunjene.",font=("Helvetica", 18))
        else:
            self.status_header_label = ctk.CTkLabel(self.subframe, text="Pogreska pri punjenju grupa.",font=("Helvetica", 18), text_color="red")
        self.status_header_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")

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
            cours_name_entry: ctk.CTkEntry = self.controller.cours_frame.cours_name_entry
            cours_name = cours_name_entry.get()
            if cours_name=="":
                cours_name = "predmet"

            cours_number_entry: ctk.CTkEntry = self.controller.cours_frame.cours_number_entry
            cours_number = cours_number_entry.get()
            if cours_number=="":
                cours_number = "smjer"

            GenErrorDetailsWorkbook(self.logger, weight_errors, fill_errors)

            dest_dir = Path.home() / "Downloads"
            copy("data/Error_detailes.xlsx", dest_dir)
            os.unlink("data/Error_detailes.xlsx")
            new_name = f"{dest_dir}/{cours_name}-{cours_number}-Error_detailes.xlsx"
            move(f"{dest_dir}/Error_detailes.xlsx", new_name)

        except Exception:
            self.logger.exception("Error with downloading Error_detailes.xlsx")
        
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
            self.logger.critical("Error when moving excel result file to downloads.")
        self.button_2.configure(text="Preuzeto", text_color="green")
        self.button_2.after(1000, self.ResetDownloadButton_2)