from excel_functions.fill_groups_results import GenErrorDetailsWorkbook, GenResultsWorkbook
from labgenpackage.participants_parser import pars_cours_participants
from excel_functions.repeat_students import get_exempt_students
from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.schedule_scraper import schedule_scraper
from labgenpackage.weight_generator import weight_generator
from labgenpackage.fill_groups import fill_groups
from labgenpackage.classes import Student, Group
from customtkinter import filedialog
from gui.util import BrowseAction
from threading import Thread

import customtkinter as ctk
import gui.settings as settings
import logging, os, gui.util as util

class FillGroupsFrame(ctk.CTkFrame):
    def __init__(self, master):
        from gui.group_gen.right_frame import RightFrame
        super().__init__(master)

        self.controller:RightFrame = master    # in case ctk widgets from other sections have to be accessed
        logger = logging.getLogger("my_app.group_gen.fill_groups")
        logger.setLevel("INFO")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        
        self.section_title_label = ctk.CTkLabel(self, text="Ispuna grupa", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="nw")

        self.alfa_prio_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.slider_event)
        self.alfa_prio_slider.configure(number_of_steps=20)
        self.alfa_prio_slider.set(0)
        self.alfa_prio_slider.grid(row=1, column=0, padx=10, pady=(30, 0), sticky="s")
        settings.alfa_prio_lvl = int(self.alfa_prio_slider.get())
        self.alfa_prio_label = ctk.CTkLabel(self, text=f"Abecedni prioritet: {settings.alfa_prio_lvl}")
        self.alfa_prio_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="n")

        self.fill_groups_button = ctk.CTkButton(self,width=60 , text="Pokreni", command=self.FillGroups_setup)  # button to start main task setup
        self.fill_groups_button.grid(row=3, column=0, padx=10, pady=10, sticky="n")

        self.exempt_label = ctk.CTkLabel(self, text='Priznati stare labove:')
        self.exempt_label.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        self.exempt_checkbox = ctk.CTkCheckBox(self, text='', width=24, command=self.eval_exempt_checkbox_event_handler, variable=settings.exempting_students, onvalue=True, offvalue=False)
        self.exempt_checkbox.grid(row=0, column=2, padx=(5,10), pady=10, sticky='nw')

        # subframe for satus display
        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=0, column=3, rowspan=4, padx=10, pady=10,sticky="wens")
        self.default_status_label = ctk.CTkLabel(self.subframe, text="Postavite sve ulazne podatke za pokrenuti.")
        self.default_status_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_columnconfigure(1, weight=1)
        self.subframe.grid_rowconfigure(0, weight=1)

    # sync slider label and slider value
    def slider_event(self,value):
        settings.alfa_prio_lvl = int(value)
        self.alfa_prio_label.configure(text=f"Abecedni prioritet: {settings.alfa_prio_lvl}")

    def eval_exempt_checkbox_event_handler(self):
        self.controller.repeat_students_frame.eval_exempt_checkbox_event()
        self.eval_exempt_checkbox_event()

    def eval_exempt_checkbox_event(self):
        if settings.exempting_students.get():
            logger = logging.getLogger("my_app.group_gen.fill_groups")

            self.exempt_subframe = ctk.CTkFrame(self)
            self.exempt_subframe.grid(row=1, column=1, columnspan=2, rowspan=3, padx=10, pady=(0,10),sticky="wens")

            self.exempt_file_label = ctk.CTkLabel(self.exempt_subframe, text='Tablica sa ponavljacima:')
            self.exempt_file_label.grid(row=0, column=0, padx=10, pady=5, sticky='n')

            self.exempt_file_entry = ctk.CTkEntry(self.exempt_subframe, placeholder_text='Excel datoteka')
            self.exempt_file_entry.configure(state='readonly')
            self.exempt_file_entry.grid(row=1, column=0, padx=10, pady=(0,5), sticky='n')

            self.exempt_file_browse_button = ctk.CTkButton(self.exempt_subframe, width=60 , text='Pretrazi', command=lambda:BrowseAction(('Excel files', '*.xlsx *.xls'),self.exempt_file_entry,logger))
            self.exempt_file_browse_button.grid(row=2, column=0, padx=10, pady=5, sticky='n')
        else:
            self.exempt_subframe.destroy()
    
    # ask user if he wants to run the main section even if the number of places is smaller than the number of students
    def CheckIfUserWantsToContinue(self)->bool:
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
        util.ClearSubframe(self.subframe)
        self.label_question = ctk.CTkLabel(self.subframe, text="Zadatak prekinut")
        self.label_question.grid(row=0,column=0, columnspan=2, padx=10, pady=10)
        self.subframe.grid_rowconfigure(0, weight=1)

    # display error msg in subframe if missing input data
    def MissingData(self):
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
        logger = logging.getLogger("my_app.group_gen.fill_groups")

        self.fill_groups_button.grid_remove()
        util.ClearSubframe(self.subframe)

        if settings.working:    # only one section can run at a time. This prevents unpredictable errors. - temporary fix
            logger.warning("Already runing another section! Cant upload new groups.")
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Vec je pokrenuta druga sekcija.\nSacekajte dok ne zavrsi sa izvodenjem.", text_color="red")
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

        exempt_file = None
        if settings.exempting_students.get():
            exempt_file = self.exempt_file_entry.get()
            if not exempt_file:
                logger.warning("Missing exempt file.")
                self.warning_label = ctk.CTkLabel(self.subframe, text=f"Nedostaje datoteka sa oslobodenim studentima.", text_color="red")
                self.warning_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
                settings.working = False
                self.fill_groups_button.grid()
                return
            
        # check if sufficient space is available in loaded groups
        if settings.total_places < len(settings.cours_participants_global) and not settings.continue_answer:
            logger.warning("Not enough space in groups!")
            self.CheckIfUserWantsToContinue()
            settings.working = False
            self.fill_groups_button.grid()
            return
        settings.continue_answer = False

        try:
            self.controller.cours_frame.save_data()
            self.controller.controller.controller.table_gen.cours_frame.set_entries()
        except Exception as e:
            e.add_note('Failed saving to data.json')
            logger.exception(e)
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Neocekivana pogresk!", text_color="red")
            self.warning_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
            settings.working = False
            self.fill_groups_button.grid()
            return

        self.main_task_progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", determinate_speed=2)
        self.main_task_progressbar.grid(row=3, column=0, padx=10, pady=10, sticky="we")
        self.main_task_progressbar.start()
        
        scrapper_thread = Thread(target=self.FillGroups_thread, args=[exempt_file])
        scrapper_thread.start()
    
    def FillGroups_thread(self,exempt_file:str):
        logger = logging.getLogger("my_app.group_gen.fill_groups")

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
            logger.info("Filling groups...")
            exempt_students:list[int] = []
            if settings.exempting_students.get():
                exempt_students = get_exempt_students(exempt_file)
            
            while running and counter<=100:
                logger.info(f"///------------------------------------------------------------------///")
                logger.info(f"Now running attempt {counter}.")
                #Get cours participants
                try:
                    logger.info("Starting participants parser!")   
                    cours_participants_local, _ = pars_cours_participants(data_dir_path="data")
                    cours_participants_copy = cours_participants_local.copy()   # a shallow copy is needed to preserve the results as data is poped from the dict
                    logger.info(f"Found {len(cours_participants_local)} students in participants file.")
                except TypeError:
                    logger.exception("Failed parsing participants!")
                    raise
                
                #Get lab group schedule
                try:
                    logger.info("Starting schedule parser!")
                    groups_local, _, _ = pars_schedule_file()
                    numofgroups:int = 0
                    day: str
                    for day in groups_local:
                        numofgroups += len(groups_local[day])
                        logger.debug(f"Found {len(groups_local[day])} groups for {day}")
                    logger.info(f"Found {numofgroups} groups in total!")
                except Exception:
                    logger.error('Failed parsing schedule!')
                    raise

                #Get schedule for every student
                try:
                    logger.info("Parsing all student scheduels.")
                    schedule_scraper(cours_participants_local, False)
                except Exception:
                    logger.error("Error when scraping schedule!")
                    raise
                
                #Generate starting weights; weight_errors are students that cant join any group at all
                try:
                    logger.info("Generating starting weights.")
                    weight_errors = weight_generator(cours_participants_local, groups_local, settings.alfa_prio_lvl)
                except Exception:
                    logger.error("Error generating starting weights!")
                    raise
                
                # fill groups with students
                logger.info("Filling groups...")
                success, fill_errors = fill_groups(cours_participants_local, groups_local, exempt_students)
                if success:
                    running = False
                    logger.info(f"///------------------------------------------------------------------///")
                    logger.info("/// SUMMARY:")
                    logger.info("Successfully filled out all groups with no students remaining!")
                    for groups_on_day in groups_local.values():
                        for group in groups_on_day:
                            logger.info(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
                            logger.info("------------------------------------------------------------------")
                else:
                    logger.warning("Failed assigning all students to a group.")
                    counter += 1
            
            # display results of fill_groups
            settings.cours_participants_result = cours_participants_copy
            self.LoadStatus(success, weight_errors, fill_errors, exempt_students)
            self.main_task_progressbar.stop()
            self.main_task_progressbar.destroy()
            self.fill_groups_button.grid()
            settings.working = False

        except ValueError as e:
            logger.warning(f"Bad exempt file: {e}")
            logger.exception(e)
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Datoteka sa oslobodenim studentima nije ispravna.", text_color="red")
            self.warning_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
            self.fill_groups_button.grid()
            self.main_task_progressbar.destroy()
            settings.working = False
            return
        except Exception as e:
            logger.error("Error filling groups!")
            logger.exception(e)
            self.LoadStatus(success, weight_errors, fill_errors, exempt_students)
            self.fill_groups_button.grid()
            self.main_task_progressbar.destroy()
            settings.working = False
            return
    
    def LoadStatus(self,success:bool, weight_errors:list[Student], fill_errors:list[Student], exempt_students:list[int]):
        logger = logging.getLogger("my_app.group_gen.fill_groups")
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
            self.button_3 = ctk.CTkButton(self.errorsubframe, width=60, text="Preuzmi", command=lambda:self.CopyErrorWeightsToDownloads(weight_errors,fill_errors,logger))
            self.button_3.grid(row=2, column=0, columnspan=2, padx=(150,20), pady=(0, 5), sticky="e")

        self.label_6 = ctk.CTkLabel(self.subframe, text="Excel datoteka sa popunjenim grupama:")
        self.label_6.grid(row=2, column=0, padx=(20,0), pady=10, sticky="w")
        self.button_2 = ctk.CTkButton(self.subframe, width=60, text="Preuzmi", command=lambda:self.CopyFilledGroupsToDownloads(exempt_students,logger))
        self.button_2.grid(row=2, column=0, columnspan=2, padx=(120,0), pady=10, sticky="")

        self.subframe.grid_columnconfigure(0, weight=1)
        self.subframe.grid_rowconfigure(0, weight=0)

    def CopyErrorWeightsToDownloads(self,weight_errors:list[Student],fill_errors:list[Student], logger: logging.Logger):
        try:
            GenErrorDetailsWorkbook(self.logger, weight_errors, fill_errors)

            util.CopyAndRename(srcname="Error_detailes.xlsx", dstname="Greske_pri_punjenju_grupa")

            os.unlink("data/Error_detailes.xlsx")
            
            self.button_3.configure(text="Preuzeto", text_color="green")
            self.button_3.after(2000, lambda: util.ResetButton(self.button_3, "Preuzmi", "white"))

        except Exception:
            self.button_3.configure(text="Pogreska", text_color="red")
            self.button_3.after(2000, lambda: util.ResetButton(self.button_3, "Preuzmi", "white"))
            logger.exception("Error with downloading Error_detailes.xlsx")
        
    def CopyFilledGroupsToDownloads(self, exempt_students:list[int], logger:logging.Logger):
        try:
            GenResultsWorkbook(exempt_students)

            util.CopyAndRename(srcname="Filled_Groups.xlsx", dstname="Popunjene_Grupe")

            os.unlink("data/Filled_Groups.xlsx")
            
            self.button_2.configure(text="Preuzeto", text_color="green")
            self.button_2.after(2000, lambda: util.ResetButton(self.button_2, "Preuzmi", "white"))

        except Exception as e:
            self.button_2.configure(text="Pogreska", text_color="red")
            self.button_2.after(2000, lambda: util.ResetButton(self.button_2, "Preuzmi", "white"))
            logger.critical("Error when moving excel result file to downloads.")
            logger.critical(e)