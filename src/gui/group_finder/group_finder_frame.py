from gui.util import ValidateDate
from threading import Thread
from labgenpackage.schedule_scraper import schedule_scraper
from gui.group_finder.finder_setup import GroupFinder_setup

from gui.util import BrowseAction
from gui.util import ResetButton

import gui.settings as settings
import customtkinter as ctk
import logging, re

# This frame has no special function, its contents are used by other sections. The user doesnt have to fill out its data.
class GroupFinderFrame(ctk.CTkFrame):
    def __init__(self, master):
        from gui.app_frame import TableGen

        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)

        self.controller: TableGen = master
        logger = logging.getLogger('my_app.group_finder')
        logger.setLevel("INFO")

        self.section_title_label = ctk.CTkLabel(self, text='Nadoknade', font=('Helvetica', 23))
        self.section_title_label.grid(row=0, column=0, padx=13, pady=10, sticky='nw')

        # ------------------------------------------------------------------
        self.subframe = ctk.CTkFrame(self)
        self.subframe.grid(row=1, column=0, padx=5, pady=5, sticky='')

        # -------------------------
        self.entry_label = ctk.CTkLabel(self.subframe, text="Ulazna datoteka:")
        self.entry_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")

        self.csv_file_entry = ctk.CTkEntry(self.subframe, placeholder_text=".csv datoteka")
        self.csv_file_entry.configure(state="readonly")
        self.csv_file_entry.grid(row=0, column=0, columnspan=5, padx=(120, 100), pady=(10, 0), sticky="we")
        
        self.browse_button = ctk.CTkButton(self.subframe, width=60 , text="Pretrazi", command=lambda:BrowseAction(("CSV Files", "*.csv"),self.csv_file_entry,logger))
        self.browse_button.grid(row=0, column=4, padx=(0, 25), pady=(10, 0), sticky="e")

        # -------------------------
        self.v_date = (self.register(self.date_callback))

        self.label_1 = ctk.CTkLabel(self.subframe, text='Naci termin u rasponu:')
        self.label_1.grid(row=1, column=0, padx=(10,5), pady=(10, 0), sticky='w')

        self.label_2 = ctk.CTkLabel(self.subframe, text='od - ')
        self.label_2.grid(row=1, column=1, padx=(0,5), pady=(10, 0), sticky='')
        self.start_date_entry = ctk.CTkEntry(self.subframe, validate='all')
        self.start_date_entry.grid(row=1, column=2, padx=(0, 5), pady=(10, 0), sticky='')
        self.start_date_entry.configure(placeholder_text='dd.mm.yyyy', validatecommand=(self.v_date, '%P', self.start_date_entry))

        self.label_3 = ctk.CTkLabel(self.subframe, text='do - ')
        self.label_3.grid(row=1, column=3, padx=(0,5), pady=(10, 0), sticky='w')
        self.end_date_entry = ctk.CTkEntry(self.subframe, validate='all')
        self.end_date_entry.grid(row=1, column=4, padx=(0, 10), pady=(10, 0), sticky='we')
        self.end_date_entry.configure(placeholder_text='dd.mm.yyyy', validatecommand=(self.v_date, '%P', self.end_date_entry))

        # -------------------------
        self.finde_groups_button = ctk.CTkButton(self.subframe, width=60 , text="Odredi grupe", command=lambda: GroupFinder_setup(self))
        self.finde_groups_button.grid(row=2, column=0, padx=(10,5), pady=10)

        self.subframe2 = ctk.CTkFrame(self.subframe)
        self.subframe2.grid(row=2, column=1, columnspan=4, padx=(5,10), pady=10, sticky="nsew")

        self.status_label = ctk.CTkLabel(self.subframe2, text="")
        self.status_label.grid(row=0, column=0, padx=5, pady=5)

        self.participants_file_label = ctk.CTkLabel(self.subframe2, text="Trenutno ucitana datoteka: NaN")
        self.participants_file_label.grid(row=1, column=0, padx=5, pady=(0,5))

        self.num_of_groups_label = ctk.CTkLabel(self.subframe2, text="Broj dostupnih grupa: Nan")
        self.num_of_groups_label.grid(row=2, column=0, padx=5, pady=(0,5))

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
    
    def HandleFGButton(self):
        finde_groups_thread = Thread(target=GroupFinder_setup, args=[self])
        finde_groups_thread.start()

    def DoneWorking(self):
        self.progressbar.stop()
        self.progressbar.destroy()
        self.finde_groups_button.grid()
        settings.working = False

    def SetProgressBar(self):
        self.progressbar = ctk.CTkProgressBar(self.subframe, width=100, orientation='horizontal', mode='determinate', determinate_speed=2)
        self.progressbar.grid(row=2, column=0, padx=(10,5), pady=10)