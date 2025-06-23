from gui.participants_frame import ParticipantsFrame
from gui.cours_frame import CoursFrame
from gui.scraper_frame import ScraperFrame

import customtkinter as ctk
import logging, json

class RightFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        #self.grid_rowconfigure(3, weight=1)

        self.controller = master    # used to access parent widget

        #Expected data is dict {"cours", "cours_number", "startdate", "enddate"}
        try:
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
        except FileNotFoundError:   # if no data.json file is found set default values
            logger.warning("The file 'data/data.json' was not found.")
            data = {"cours":"", "cours_number":"", "startdate":"","enddate":""}
            pass
        except IOError:     # App will close
            logger.critical("Error opening data.json file!")
            raise
        except Exception:   # App will close
            logger.critical("Unexpected error with data.jsonfile !")
            raise
            
        # init 'CoursFrame'
        self.cours_frame = CoursFrame(self,data["cours"], data["cours_number"])
        self.cours_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.participants_frame = ParticipantsFrame(self,logger)
        self.participants_frame.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

        self.scraper_frame = ScraperFrame(self,data["startdate"], data["enddate"], logger)
        self.scraper_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky="ew")

        # self.fill_groups_frame = FillGroupsFrame(self)
        # self.fill_groups_frame.grid(row=3, column=0, padx=10, pady=(0,10), sticky="nsew")
