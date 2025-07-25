from customtkinter import filedialog
from pathlib import Path
from shutil import copy
from os import path

import gui.settings as settings
import customtkinter as ctk
import logging, glob

class RepeatStudentsFrame(ctk.CTkFrame):
    def __init__(self, master):
        from gui.right_frame import RightFrame
        super().__init__(master)

        self.controller: RightFrame = master
        logger = logging.getLogger('my_app.group_gen')

        self.section_title_label = ctk.CTkLabel(self, text='Ponavljači', font=('Helvetica', 23))
        self.section_title_label.grid(row=0, column=0, padx=10, pady=(15, 0), sticky='nw')

        self.exempt_label = ctk.CTkLabel(self, text='Priznati stare labove:')
        self.exempt_label.grid(row=1, column=0, padx=10, pady=5, sticky='nw')

        self.exempt_checkbox = ctk.CTkCheckBox(self, text='', width=230, command=self.eval_exempt_checkbox_event, variable=settings.exempting_students, onvalue=True, offvalue=False)
        self.exempt_checkbox.grid(row=1, column=1, padx=(5,10), pady=5, sticky='nw')

        self.columnconfigure(1, weight=1)

        
    def eval_exempt_checkbox_event(self):
        if settings.exempting_students.get():    
            self.rules_subframe = ctk.CTkFrame(self)
            self.rules_subframe.grid(row=2, column=0, columnspan=2, padx=10, pady=(0,10), sticky='nswe')

            self.get_old_file_label = ctk.CTkLabel(self.rules_subframe, text='Tablica prosle ak. god.:')
            self.get_old_file_label.grid(row=0, column=0, padx=5, pady=5, sticky='nw')

            self.get_old_file_entry = ctk.CTkEntry(self.rules_subframe, placeholder_text='Excel datoteka')
            self.get_old_file_entry.configure(state='readonly')
            self.get_old_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nwe')

            self.get_old_file_browse_button = ctk.CTkButton(self.rules_subframe, width=60 , text='Pretrazi', command=lambda:self.browse_action(self.get_old_file_entry))
            self.get_old_file_browse_button.grid(row=0, column=2, padx=5, pady=5, sticky='nw')

            self.passed_exemption_label = ctk.CTkLabel(self.rules_subframe, text='Oslobođeni ako su položili prethodne godine:')
            self.passed_exemption_label.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky='nw')

            self.passed_exemption_checkbox = ctk.CTkCheckBox(self.rules_subframe, text='', width=24, variable=settings.freed_if_passed_last, onvalue=True, offvalue=False)
            self.passed_exemption_checkbox.grid(row=1, column=1, columnspan=2, padx=(55,0), pady=(0,5), sticky='n')

            self.conditional_exemption = ctk.CTkLabel(self.rules_subframe, text='Oslobođeni ako su položili barem                 puta.')
            self.conditional_exemption.grid(row=2, column=0, columnspan=2, padx=5, pady=(0,5), sticky='nw')

            self.num_of_needed_passes_entry = ctk.CTkEntry(self.rules_subframe, width=35)
            self.num_of_needed_passes_entry.grid(row=2, column=1, padx=(15,5), pady=(0,5), sticky='n')

            self.get_repeat_students_button = ctk.CTkButton(self.rules_subframe, width=125 , text="Preuzmi ponavljače", command=get_repeat_students)
            self.get_repeat_students_button.grid(row=5, column=0, columnspan=3, padx=10, pady=15)

        else:
            self.rules_subframe.destroy()

    def browse_action(self,entry: ctk.CTkEntry):
        filename = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx *.xls')])
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0,filename)
        entry.configure(state='readonly')


def get_repeat_students():
    pass