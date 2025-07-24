from gui.participants_frame import ParticipantsFrame
from gui.cours_frame import CoursFrame
from gui.scraper_frame import ScraperFrame
from gui.fill_groups_frame import FillGroupsFrame

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
        self.cours_frame = CoursFrame(self)
        self.cours_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.participants_frame = ParticipantsFrame(self,logger)
        self.participants_frame.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

        self.scraper_frame = ScraperFrame(self, logger)
        self.scraper_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky="ew")

        self.fill_groups_frame = FillGroupsFrame(self,logger)
        self.fill_groups_frame.grid(row=3, column=0, padx=10, pady=(0,10), sticky="nsew")
