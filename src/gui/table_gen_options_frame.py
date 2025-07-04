import gui.settings as settings
import customtkinter as ctk
import logging

# This frame has no special function, its contents are used by other sections. The user doesnt have to fill out its data.
class TableGenOptionsFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=2)

        self.controller = master    # in case ctk widgets from other sections have to be accessed
        self.logger = logger

        self.section_title_label = ctk.CTkLabel(self, text="Postavke", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, columnspan=2, padx=13, pady=(10, 0), sticky="nw")

        self.ex_lable_subframe = ctk.CTkFrame(self)
        self.ex_lable_subframe.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nwe")
        
        
        # --------------------------
        # number of lab exercises and required attendance
        self.num_lab_attend_subframe = ctk.CTkFrame(self.ex_lable_subframe, width=400)
        self.num_lab_attend_subframe.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nwe")
        self.num_lab_attend_subframe.grid_columnconfigure(4, weight=1)
        self.num_labexc_lable = ctk.CTkLabel(self.num_lab_attend_subframe, text="Broj vjezbi:")
        self.num_labexc_lable.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.vcmd = (self.register(self.callback))
        self.num_labexc_entry = ctk.CTkEntry(self.num_lab_attend_subframe, width=45, justify="center", validate='all', validatecommand=(self.vcmd, '%P'))
        self.num_labexc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.attendance_lable = ctk.CTkLabel(self.num_lab_attend_subframe, text="-  Obavezna prisutnost:")
        self.attendance_lable.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

        self.vcmd1 = (self.register(self.callback1))
        self.attendance_entry = ctk.CTkEntry(self.num_lab_attend_subframe, width=45, justify="center", validate='all', validatecommand=(self.vcmd1, '%P'))
        self.attendance_entry.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

        self.attendance_lable2 = ctk.CTkLabel(self.num_lab_attend_subframe, text="/ NaN")
        self.attendance_lable2.grid(row=0, column=4, padx=5, pady=5, sticky="nw")

        # --------------------------
        # custom exercise lables
        self.custom_exlables_subframe = ctk.CTkFrame(self.ex_lable_subframe, width=400)
        self.custom_exlables_subframe.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nwe")

        self.custom_exlables_lable = ctk.CTkLabel(self.custom_exlables_subframe, text="Rucno postavljanje labela za zadatke:")
        self.custom_exlables_lable.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.custom_exlables_check_var = ctk.StringVar(value="off")
        self.custom_exlables_checkbox = ctk.CTkCheckBox(self.custom_exlables_subframe, text="", width=24, command=self.eval_custom_exlables_checkbox_event,variable=self.custom_exlables_check_var, onvalue="on", offvalue="off")
        self.custom_exlables_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        # self.custom_exlables_entry = ctk.CTkEntry(self.custom_exlables_subframe, placeholder_text="Unesite zarezom odvojene vrijednosti. Npr: zad1, vj2, test3, itd.", width=400, validate='all', validatecommand=(vcmd2, '%P'))
        # self.custom_exlables_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky="nwe")

        # --------------------------
        # evaluation of exercise 0 or 1
        self.evalex0_subframe = ctk.CTkFrame(self.ex_lable_subframe, width=400)
        self.evalex0_subframe.grid(row=2, column=0, padx=5, pady=5, sticky="nwe")

        self.eval_ex0_lable = ctk.CTkLabel(self.evalex0_subframe, text="Prva vjezba se ne ocjenjuje:")
        self.eval_ex0_lable.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.ex0_check_var = ctk.StringVar(value="off")
        self.ex0_checkbox = ctk.CTkCheckBox(self.evalex0_subframe, text="", width=24, command=self.eval_ex0_checkbox_event,variable=self.ex0_check_var, onvalue="on", offvalue="off")
        self.ex0_checkbox.grid(row=0, column=1, padx=5, pady=5, sticky="nw")


    def callback(self, P):
        if str.isdigit(P):
            self.attendance_lable2.configure(text=f"/ {P}")
            self.attendance_entry.delete(0)
            self.attendance_entry.insert(0,P)
            return True
        elif P == "":
            self.attendance_lable2.configure(text=f"/ NaN")
            return True
        else: return False

    def callback1(self, P):
        if P == "": return True
        if not str.isdigit(self.num_labexc_entry.get()): return False
        if not str.isdigit(P): return False
        if int(P) <= int(self.num_labexc_entry.get()): return True
        else: return False
    
    def callback2(self, P):
        return True
    
    def eval_custom_exlables_checkbox_event(self):
        if self.custom_exlables_check_var.get() == "on":
            self.vcmd2 = (self.register(self.callback2))
            self.custom_exlables_entry = ctk.CTkEntry(self.custom_exlables_subframe, placeholder_text="Unesite zarezom odvojene vrijednosti. Npr: zad1, vj2, test3, itd.", width=400, validate='all', validatecommand=(self.vcmd2, '%P'))
            self.custom_exlables_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky="nwe")
        elif self.custom_exlables_check_var.get() == "off":
            self.custom_exlables_entry.destroy()
    
    def eval_ex0_checkbox_event(self):
        if self.ex0_check_var.get() == "on":
            self.lab0_label = ctk.CTkLabel(self.evalex0_subframe, text="Koristiti nultu vjezbu (lab0):")
            self.lab0_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
            self.lab0_check_var = ctk.StringVar(value="off")
            self.lab0_checkbox = ctk.CTkCheckBox(self.evalex0_subframe, text="", width=24, command=self.eval_lab0_checkbox_event,variable=self.lab0_check_var, onvalue="on", offvalue="off")
            self.lab0_checkbox.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        elif self.ex0_check_var.get() == "off":
            self.lab0_label.destroy()
            self.lab0_checkbox.destroy()
    
    def eval_lab0_checkbox_event(self):
        pass