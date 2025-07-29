from gui.table_gen_options_frame import TableGenOptionsFrame
from gui.groups_frame import GroupsFrame
from gui.cours_frame import CoursFrame
from gui.right_frame import RightFrame
from pathlib import Path

import customtkinter as ctk
import gui.settings as settings
import logging, json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        logger = logging.getLogger("my_app")
        logger.setLevel("INFO")

        logger.info("Startup setup.")
        settings.init()
        Path("data").mkdir(exist_ok=True)

        #Expected data is dict {"cours", "cours_number", "acad_year", "startdate", "enddate"}
        try:
            logger.info("Loading data.json...")
            with open("data/data.json", "r") as file:
                data:dict[str:str] = json.load(file)
                settings.cours_name = data["cours"]
                settings.cours_number = data["cours_number"]
                settings.acad_year = data["acad_year"]
                settings.start_date = data["start_date"]
                settings.end_date = data["end_date"]
            logger.debug(f"Loaded values: {settings.cours_name}, {settings.cours_number}, {settings.acad_year}, {settings.start_date}, {settings.end_date}")
            logger.info("Data loaded from data.json.")
        except FileNotFoundError:   # if no data.json file is found set default values
            logger.warning("The file 'data/data.json' was not found.")
            logger.info(f"Creating default data.json file.")
            logger.debug(f"Creating default data json with: {settings.default_data_json}")
            data = settings.default_data_json
            json_object = json.dumps(data, indent=4)
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

        self.tab_view = TabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=3, pady=3, sticky="n")

class TabView(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master)

        # create tabs
        self.add("groups_gen")
        self.add("table_gen")

        # add widgets on tabs
        self.group_gen = GroupsGen(master=self.tab("groups_gen"))
        self.group_gen.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")
        self.table_gen = TableGen(master=self.tab("table_gen"))
        self.table_gen.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        
class GroupsGen(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame):
        super().__init__(master)

        logger = logging.getLogger("my_app.group_gen")
        logger.setLevel("INFO")

        self.controller: TabView = master.master

        #init groups frame
        self.schedule_frame = GroupsFrame(self,logger)
        self.schedule_frame.grid(row=0, column=0, padx=(5,0), pady=0, sticky="nswe")

        #init right frame - containes all other sections
        self.right_frame = RightFrame(self,logger)
        self.right_frame.grid(row=0, column=1, padx=(0,5), pady=0, sticky="nsew")

class TableGen(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame):
        super().__init__(master)

        logger = logging.getLogger("my_app.table_gen")
        logger.setLevel("INFO")

        self.controller: TabView = master.master

        self.cours_frame = CoursFrame(self, logger)
        self.cours_frame.grid(row=0,column=0, padx=5, pady=0, sticky="we")

        self.table_gen_options_frame = TableGenOptionsFrame(self)
        self.table_gen_options_frame.grid(row=1,column=0, padx=5, pady=(5,0), sticky="we")

        self.grid_columnconfigure(0, weight=1)
        self.table_gen_options_frame.grid_columnconfigure(0, weight=1)