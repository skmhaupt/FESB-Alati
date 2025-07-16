from customtkinter import filedialog
from excel_functions.lab_table import gen_tables
from gui.util import ResetButton

import gui.settings as settings
import customtkinter as ctk
import logging

# This frame has no special function, its contents are used by other sections. The user doesnt have to fill out its data.
class TableGenOptionsFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)

        self.controller = master    # in case ctk widgets from other sections have to be accessed
        self.logger = logger

        self.section_title_label = ctk.CTkLabel(self, text="Postavke", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, columnspan=2, padx=13, pady=(10, 0), sticky="nw")

        self.settings_subframe = ctk.CTkFrame(self)
        self.settings_subframe.grid(row=1, column=0, padx=5, pady=5, sticky="nwe")
        
        self.settings_subframe.grid_columnconfigure(0, weight=1)
        
        # ----------------------------------------------------------------------------------------------------
        # validations commands for entrys 
        self.v_num_labex = (self.register(self.num_labex_callback))
        self.v_attendance = (self.register(self.attendance_callback))
        self.v_custom_exlabels = (self.register(self.custom_exlabels_callback))
        self.v_max_points = (self.register(self.max_points_callback))
        self.v_min_average_required = (self.register(self.min_average_required_callback))

        # ----------------------------------------------------------------------------------------------------
        # number of lab exercises and required attendance
        self.num_lab_attend_subframe = ctk.CTkFrame(self.settings_subframe)
        self.num_lab_attend_subframe.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nwe")
        
        self.num_labexc_label = ctk.CTkLabel(self.num_lab_attend_subframe, text="Broj vjezbi:")
        self.num_labexc_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.num_labexc_entry = ctk.CTkEntry(self.num_lab_attend_subframe, width=45, justify="center", validate='all', validatecommand=(self.v_num_labex, '%P'))
        self.num_labexc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.attendance_label = ctk.CTkLabel(self.num_lab_attend_subframe, text="Obavezna prisutnost:")
        self.attendance_label.grid(row=0, column=2, padx=(40, 5), pady=5, sticky="nw")

        self.attendance_entry = ctk.CTkEntry(self.num_lab_attend_subframe, width=45, justify="center", validate='all', validatecommand=(self.v_attendance, '%P'))
        self.attendance_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

        self.attendance_label2 = ctk.CTkLabel(self.num_lab_attend_subframe, anchor=ctk.W, width=70, text="/ NaN")
        self.attendance_label2.grid(row=0, column=4, padx=5, pady=5, sticky="nw")
        
        self.num_lab_attend_subframe.grid_columnconfigure(4, weight=1)

        # ----------------------------------------------------------------------------------------------------
        # custom exercise labels
        self.custom_exlabels_subframe = ctk.CTkFrame(self.settings_subframe)
        self.custom_exlabels_subframe.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nwe")

        self.custom_exlabels_label = ctk.CTkLabel(self.custom_exlabels_subframe, text="Rucno postavljanje labela za vjezbe:")
        self.custom_exlabels_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.custom_exlabels_checkbox = ctk.CTkCheckBox(self.custom_exlabels_subframe, text="", width=24, command=self.eval_custom_exlabels_checkbox_event,variable=settings.using_custom_exlabels, onvalue=True, offvalue=False)
        self.custom_exlabels_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.custom_exlabels_subframe.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------------------------------------------------------
        # evaluation of exercise 0 or 1
        self.evalex0_subframe = ctk.CTkFrame(self.settings_subframe)
        self.evalex0_subframe.grid(row=2, column=0, padx=5, pady=(5,0), sticky="nwe")

        self.no_eval_ex0_label = ctk.CTkLabel(self.evalex0_subframe, text="Prva vjezba se ne ocjenjuje:")
        self.no_eval_ex0_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.no_eval_ex0_checkbox = ctk.CTkCheckBox(self.evalex0_subframe, text="", width=24, command=self.eval_ex0_checkbox_event,variable=settings.no_eval_ex0, onvalue=True, offvalue=False)
        self.no_eval_ex0_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        # ----------------------------------------------------------------------------------------------------
        # errors subframe
        self.errors_subframe = ctk.CTkFrame(self.settings_subframe)
        self.errors_subframe.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="nwe")

        self.error_label = ctk.CTkLabel(self.errors_subframe, text=" ", text_color="red")
        self.error_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        # ----------------------------------------------------------------------------------------------------
        # preview subframe
        self.preview_subframe = ctk.CTkFrame(self.settings_subframe)
        self.preview_subframe.grid(row=1, column=1,rowspan=2, padx=5, pady=5, sticky="nwe")

        self.preview_title_label = ctk.CTkLabel(self.preview_subframe, text="Pretpregled:", font=("Helvetica", 15))
        self.preview_title_label.grid(row=0, column=0, padx=10, pady=(5,0), sticky="nw")
        
        self.preview_label = ctk.CTkLabel(self.preview_subframe, text="Prezime i ime | ... | grupe")
        self.preview_label.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nw")

        # ----------------------------------------------------------------------------------------------------
        # grade subframe subframe
        self.grade_subframe = ctk.CTkFrame(self.settings_subframe)
        self.grade_subframe.grid(row=3, column=0, padx=5, pady=(5,0), sticky="nwe")

        self.max_points_label = ctk.CTkLabel(self.grade_subframe, text="Max broj bodova na ulaznom/izlaznom:")
        self.max_points_label.grid(row=0, column=0, padx=5, pady=(5,0), sticky="nw")
        
        self.max_points_entry = ctk.CTkEntry(self.grade_subframe, width=45, justify="center", validate='all', validatecommand=(self.v_max_points, '%P'))
        self.max_points_entry.grid(row=0, column=1, padx=5, pady=(5,0), sticky="nw")

        self.dont_use_failed_points_label = ctk.CTkLabel(self.grade_subframe, text="Ne polozeni ulazni/izlazni vrijede 0 boda:")
        self.dont_use_failed_points_label.grid(row=1, column=0, padx=5, pady=(5,0), sticky="nw")
        
        self.dont_use_failed_points_checkbox = ctk.CTkCheckBox(self.grade_subframe, text="", width=24,variable=settings.not_using_failed_points, onvalue=True, offvalue=False)
        self.dont_use_failed_points_checkbox.grid(row=1, column=1, padx=5, pady=(5,0), sticky="nw")

        self.min_average_required_label = ctk.CTkLabel(self.grade_subframe, text="Potrebni prosjek za prolaz [%]:")
        self.min_average_required_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        
        self.min_average_required_entry = ctk.CTkEntry(self.grade_subframe, width=45, justify="center", validate='all', validatecommand=(self.v_min_average_required, '%P'))
        self.min_average_required_entry.grid(row=2, column=0, padx=(5,10), pady=5, sticky="ne")
        
        self.min_average_required_preview_label = ctk.CTkLabel(self.grade_subframe, text="NaN / NaN")
        self.min_average_required_preview_label.grid(row=2, column=1, padx=5, pady=5, sticky="nw")

        # ----------------------------------------------------------------------------------------------------
        # repeat students
        self.get_repeat_students_subframe = ctk.CTkFrame(self.settings_subframe)
        self.get_repeat_students_subframe.grid(row=4, column=0, columnspan=2, padx=5, pady=(5,0), sticky="nwe")

        self.get_repeat_students_label = ctk.CTkLabel(self.get_repeat_students_subframe, text="Odrediti ponavljace")
        self.get_repeat_students_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.get_repeat_students_checkbox = ctk.CTkCheckBox(self.get_repeat_students_subframe, text="", width=24, command=self.eval_get_repeat_students_checkbox_event, variable=settings.get_repeat_students, onvalue=True, offvalue=False)
        self.get_repeat_students_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        # ----------------------------------------------------------------------------------------------------
        # input file
        self.input_file_subframe = ctk.CTkFrame(self.settings_subframe)
        self.input_file_subframe.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nwe")

        self.input_file_label = ctk.CTkLabel(self.input_file_subframe, text="Ulazna datoteka:")
        self.input_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="")

        self.input_file_entry = ctk.CTkEntry(self.input_file_subframe, placeholder_text="Excel datoteka")
        self.input_file_entry.configure(state="readonly")
        self.input_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nwe")

        self.input_file_browse_button = ctk.CTkButton(self.input_file_subframe, width=60 , text="Pretrazi", command=lambda:self.browse_action(self.input_file_entry))
        self.input_file_browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

        self.input_file_subframe.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------------------------------------------------------
        # generate tables and errors
        self.gen_tables_button = ctk.CTkButton(self.settings_subframe, width=60, text="Generiraj Tablice", command=self.gen_tables)
        self.gen_tables_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.error_label2 = ctk.CTkLabel(self.settings_subframe, width=140, text="test", text_color="red")
        self.error_label2.grid(row=6, column=0, columnspan=2, padx=50, pady=10, sticky="ne")

        # ----------------------------------------------------------------------------------------------------
        # set default entry values
        self.max_points_entry.insert(0,"10")
        self.min_average_required_entry.insert(0,"50")

    # --------------------------------------------------------------------------------------------------------
    # callbacks for entry validations
    def num_labex_callback(self, P):
        if str.isdigit(P):
            settings.ex_num = int(P)
            self.update_min_average_required_preview_label()
            self.update_attendance_label2()
            self.update_ex_preview_label()
            return True
        elif P == "":
            settings.ex_num = 0     # default value
            self.clear_attendance_label2()
            return True
        else: return False

    def attendance_callback(self, P):
        if P == "": 
            settings.attendance = 0
            return True
        if not settings.ex_num: return False
        if not str.isdigit(P): return False
        if int(P) > settings.ex_num: return False
        else: 
            settings.attendance = int(P)
            return True
    
    def custom_exlabels_callback(self, P):
        ex_labels = str.split(P,",")
        settings.custom_ex_labels = ex_labels
        if len(ex_labels) > settings.ex_num: self.error_label.configure(text="Previse labela!")
        elif len(ex_labels) != settings.ex_num: self.error_label.configure(text="Nedovoljan broj labela!")
        else: self.error_label.configure(text="")

        new_text = "Prezime i ime"
        for ex in range(len(ex_labels)):
            new_text = new_text + f" | {ex_labels[ex].strip()}"
            if ex>9 and ex%10==0:
                new_text = new_text + "\n"
        new_text = new_text + " | Grupa"
        self.preview_label.configure(text=new_text)
        return True
    
    def max_points_callback(self, P):
        if P == "": return True
        elif str.isdigit(P):
            settings.max_test_points = int(P)
            self.update_min_average_required_preview_label()
            return True
        else: return False
    
    def min_average_required_callback(self, P):
        if P == "": return True
        elif str.isdigit(P):
            if int(P) <= 100:
                settings.min_average_required = int(P)
                self.update_min_average_required_preview_label()
                return True
        else: return False
    
    # --------------------------------------------------------------------------------------------------------
    # checkbox events
    def eval_custom_exlabels_checkbox_event(self):
        if settings.using_custom_exlabels.get():
            self.custom_exlabels_entry = ctk.CTkEntry(self.custom_exlabels_subframe, placeholder_text="Unesite zarezom odvojene vrijednosti. Npr: zad1, vj2, test3, itd.", width=400, validate='all', validatecommand=(self.v_custom_exlabels, '%P'))
            self.custom_exlabels_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky="nw")
            self.clear_preview_label()
            settings.using_lab0.set(False)
            if hasattr(self, "lab0_label") and hasattr(self, "lab0_checkbox"):
                self.destroy_lab0_widgets()
        elif not settings.using_custom_exlabels.get():
            self.custom_exlabels_entry.destroy()
            self.error_label.configure(text="")
            self.update_ex_preview_label()
            if settings.no_eval_ex0.get():
                self.create_lab0_widgets()
    
    def eval_ex0_checkbox_event(self):
        if settings.no_eval_ex0.get() and not settings.using_custom_exlabels.get():
            self.create_lab0_widgets()
        elif not settings.no_eval_ex0.get() and hasattr(self, "lab0_label") and hasattr(self, "lab0_checkbox"):
            self.destroy_lab0_widgets()
        self.update_min_average_required_preview_label()
    
    def eval_lab0_checkbox_event(self):
        self.update_ex_preview_label()
        self.update_min_average_required_preview_label()

    def eval_get_repeat_students_checkbox_event(self):
        if settings.get_repeat_students.get():
            self.get_old_file_label = ctk.CTkLabel(self.get_repeat_students_subframe, text="Tablica prosle ak. god.:")
            self.get_old_file_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

            self.get_old_file_entry = ctk.CTkEntry(self.get_repeat_students_subframe, placeholder_text="Excel datoteka")
            self.get_old_file_entry.configure(state="readonly")
            self.get_old_file_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nwe")

            self.get_old_file_browse_button = ctk.CTkButton(self.get_repeat_students_subframe, width=60 , text="Pretrazi", command=lambda:self.browse_action(self.get_old_file_entry))
            self.get_old_file_browse_button.grid(row=0, column=4, padx=5, pady=5, sticky="nw")

            self.get_repeat_students_subframe.grid_columnconfigure(3, weight=1)
        else:
            self.get_old_file_label.destroy()
            self.get_old_file_entry.destroy()
            self.get_old_file_browse_button.destroy()

    # --------------------------------------------------------------------------------------------------------
    # create/destroy widgets functions
    def create_lab0_widgets(self):
        self.lab0_label = ctk.CTkLabel(self.evalex0_subframe, text="Koristiti nultu vjezbu (lab0):")
        self.lab0_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.lab0_checkbox = ctk.CTkCheckBox(self.evalex0_subframe, text="", width=24, command=self.eval_lab0_checkbox_event,variable=settings.using_lab0, onvalue=True, offvalue=False)
        self.lab0_checkbox.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
    
    def destroy_lab0_widgets(self):
        if self.lab0_label.winfo_exists(): self.lab0_label.destroy()
        if self.lab0_checkbox.winfo_exists(): self.lab0_checkbox.destroy()

    # --------------------------------------------------------------------------------------------------------
    # update label functions
    def clear_attendance_label2(self):
        self.attendance_label2.configure(text=f"/ NaN")
    
    def update_attendance_label2(self):
        self.attendance_label2.configure(text=f"/ {settings.ex_num}")
        self.attendance_entry.delete(0)
        self.attendance_entry.insert(0,settings.ex_num)

    def clear_preview_label(self):
        new_text = "Prezime i ime | ... | Grupa"
        self.preview_label.configure(text=new_text)

    def update_ex_preview_label(self):
        if settings.using_custom_exlabels.get(): return
        if not settings.ex_num: return

        new_text = "Prezime i ime"
        if settings.using_lab0.get(): new_text = new_text + " | Lab 0"
        for ex in range(settings.ex_num):
            new_text = new_text + f" | Lab {ex+1}"
            if ex>9 and ex%10==0:
                new_text = new_text + "\n"
        new_text = new_text + " | Grupa"
        self.preview_label.configure(text=new_text)

    def update_min_average_required_preview_label(self):
        if not settings.ex_num or not settings.max_test_points or not settings.min_average_required:
            self.min_average_required_preview_label.configure(text="NaN/NaN")
        else:
            if settings.no_eval_ex0.get() and not settings.using_lab0.get(): max_cours_points = settings.max_test_points * (settings.ex_num - 1)
            else: max_cours_points = settings.max_test_points * settings.ex_num
            min_required_cours_points = settings.min_average_required / 100 * max_cours_points
            self.min_average_required_preview_label.configure(text=f"{min_required_cours_points}/{max_cours_points}")

    # --------------------------------------------------------------------------------------------------------
    # button functions
    def browse_action(self,entry: ctk.CTkEntry):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0,filename)
        entry.configure(state="readonly")

    def gen_tables(self):
        input_file = self.input_file_entry.get()
        success = gen_tables(input_file)

        if success:
            self.gen_tables_button.configure(text="Preuzeto", text_color="green")
            self.gen_tables_button.after(2000, lambda: ResetButton(self.gen_tables_button, "Preuzmi", "white"))
        else:
            self.gen_tables_button.configure(text="Pogreska", text_color="red")
            self.gen_tables_button.after(2000, lambda: ResetButton(self.gen_tables_button, "Preuzmi", "white"))