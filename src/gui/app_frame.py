from gui.table_gen_options_frame import TableGenOptionsFrame
from gui.groups_frame import GroupsFrame
from gui.cours_frame import CoursFrame
from gui.right_frame import RightFrame
from pathlib import Path

import customtkinter as ctk
import gui.settings as settings
import logging, json

class App(ctk.CTk):
    def __init__(self, logger:logging.Logger):
        super().__init__()

        #startup setup
        settings.init()
        Path("data").mkdir(exist_ok=True)

        #Expected data is dict {"cours", "cours_number", "acad_year", "startdate", "enddate"}
        try:
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
                settings.cours_name = data["cours"]
                settings.cours_number = data["cours_number"]
                settings.acad_year = data["acad_year"]
                settings.start_date = data["start_date"]
                settings.end_date = data["end_date"]
        except FileNotFoundError:   # if no data.json file is found set default values
            logger.warning("The file 'data/data.json' was not found.")
            data = settings.default_data_json
            json_object = json.dumps(data, indent=4)
            logger.info(f"Creating default data.json file.")
            with open("data/data.json", "w") as file:
                file.write(json_object)
            pass
        except IOError:     # App will close
            logger.critical("Error opening data.json file!")
            raise
        except Exception:   # App will close
            logger.critical("Unexpected error with data.jsonfile !")
            raise

        self.title("Lab generator")
        #self.geometry("1100x980")
        #self.resizable(False, False)
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = TabView(master=self,logger=logger)
        self.tab_view.grid(row=0, column=0, padx=3, pady=3, sticky="n")

class TabView(ctk.CTkTabview):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)

        # create tabs
        self.add("groups_gen")
        self.add("table_gen")

        # add widgets on tabs
        self.group_gen = GroupsGen(master=self.tab("groups_gen"),logger=logger)
        self.group_gen.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.table_gen = TableGen(master=self.tab("table_gen"),logger=logger)
        self.table_gen.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        
class GroupsGen(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame, logger: logging.Logger):
        super().__init__(master)

        self.controller: TabView = master.master
        self.logger = logger

        #init groups frame
        self.schedule_frame = GroupsFrame(self,logger)
        self.schedule_frame.grid(row=0, column=0, padx=(5,0), pady=0, sticky="nswe")

        #init right frame - containes all other sections
        self.right_frame = RightFrame(self,logger)
        self.right_frame.grid(row=0, column=1, padx=(0,5), pady=0, sticky="nsew")

class TableGen(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame, logger:logging.Logger):
        super().__init__(master)

        self.logger = logger
        self.controller: TabView = master.master

        self.cours_frame = CoursFrame(self)
        self.cours_frame.grid(row=0,column=0, padx=5, pady=0, sticky="we")

        self.table_gen_options_frame = TableGenOptionsFrame(self)
        self.table_gen_options_frame.grid(row=1,column=0, padx=5, pady=(5,0), sticky="we")

        self.grid_columnconfigure(0, weight=1)
        self.table_gen_options_frame.grid_columnconfigure(0, weight=1)