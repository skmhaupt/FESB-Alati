from gui.groups_frame import GroupsFrame
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
        self.geometry("1100x700")
        self.resizable(False, False)
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #init groups frame
        self.schedule_frame = GroupsFrame(self,logger)
        self.schedule_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nswe")

        # self.right_frame = RightFrame(self)
        # self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # self.right_frame.grid_columnconfigure(0, weight=1)
