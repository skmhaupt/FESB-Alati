from gui.table_gen_options_frame import TableGenOptionsFrame
from gui.groups_frame import GroupsFrame
from gui.cours_frame import CoursFrame
from gui.right_frame import RightFrame
from pathlib import Path

import customtkinter as ctk
import gui.settings as settings
import logging

class App(ctk.CTk):
    def __init__(self, logger:logging.Logger):
        super().__init__()

        #startup setup
        settings.init()
        Path("data").mkdir(exist_ok=True)

        self.title("Lab generator")
        self.geometry("1100x780")
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
        
class GroupsGen(ctk.CTkLabel):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)

        self.logger = logger
        self.controller = master    # in case ctk widgets from other sections have to be accessed

        #init groups frame
        self.schedule_frame = GroupsFrame(self,logger)
        self.schedule_frame.grid(row=0, column=0, padx=(5,0), pady=0, sticky="nswe")

        #init right frame - containes all other sections
        self.right_frame = RightFrame(self,logger)
        self.right_frame.grid(row=0, column=1, padx=(0,5), pady=0, sticky="nsew")

        #self.right_frame.grid_columnconfigure(0, weight=1)

class TableGen(ctk.CTkFrame):
    def __init__(self, master, logger:logging.Logger):
        super().__init__(master)

        self.logger = logger
        self.controller = master

        self.cours_frame = CoursFrame(self, settings.cours_name, settings.cours_number)
        self.cours_frame.grid(row=0,column=0, padx=5, pady=0, sticky="we")

        self.table_gen_options_frame = TableGenOptionsFrame(self,logger)
        self.table_gen_options_frame.grid(row=1,column=0, padx=5, pady=(5,0), sticky="we")

        self.grid_columnconfigure(0, weight=1)
        self.table_gen_options_frame.grid_columnconfigure(0, weight=1)