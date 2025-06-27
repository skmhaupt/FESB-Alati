from shutil import copy, move
from pathlib import Path

import gui.settings as settings
import customtkinter as ctk
import os

def ResetButton(button: ctk.CTkButton, text, color):
    button.configure(text=text, text_color=color)

def ClearSubframe(subframe: ctk.CTkFrame):
     for widget in subframe.winfo_children():   # deleting all old widgets in subframe
        widget.destroy()

    # copys src file to downloads and renames to "cours_name-cours_number-dstname"
def CopyAndRename(srcname: str, dstname: str):
    dest_dir = Path.home() / "Downloads"
    srcfile = f"data/{srcname}"
    copy(srcfile, dest_dir)

    # rename new file in downloads
    if settings.cours_name == "":
        settings.cours_name = "predmet"
    if settings.cours_number == "":
        settings.cours_number = "smjer"
    
    new_name = f"{dest_dir}/{settings.cours_name}-{settings.cours_number}-{dstname}.xlsx"
    name, extension = os.path.splitext(new_name)
    if not os.path.isfile(new_name):
        move(f"{dest_dir}/{srcname}", new_name)
    else:
        i = 1
        new_name = f"{name}({i}){extension}"
        while os.path.isfile(new_name):
            i += 1
            new_name = f"{name}({i}){extension}"
        move(f"{dest_dir}/{srcname}", new_name)