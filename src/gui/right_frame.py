from gui.repeat_students_frame import RepeatStudentsFrame
from gui.participants_frame import ParticipantsFrame
from gui.fill_groups_frame import FillGroupsFrame
from gui.scraper_frame import ScraperFrame
from gui.cours_frame import CoursFrame

import customtkinter as ctk
import logging

class RightFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        from gui.app_frame import GroupsGen
        super().__init__(master)

        self.controller: GroupsGen = master
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
            
        # init 'CoursFrame'
        self.cours_frame = CoursFrame(self, logger)
        self.cours_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.participants_frame = ParticipantsFrame(self,logger)
        self.participants_frame.grid(row=1, column=0, padx=(10,5), pady=(0,10), sticky="ew")

        self.scraper_frame = ScraperFrame(self, logger)
        self.scraper_frame.grid(row=2, column=0, padx=(10,5), pady=(0,10), sticky="ew")

        self.repeat_students_frame = RepeatStudentsFrame(self)
        self.repeat_students_frame.grid(row=1, column=1, rowspan=2, padx=(5,10), pady=(0,10), sticky='nsew')

        self.fill_groups_frame = FillGroupsFrame(self,logger)
        self.fill_groups_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0,10), sticky="nsew")
