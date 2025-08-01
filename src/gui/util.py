from customtkinter import filedialog
from shutil import copy, move
from pathlib import Path

import gui.settings as settings
import customtkinter as ctk
import os, logging, glob

def ResetButton(button: ctk.CTkButton, text, color):
    button.configure(text=text, text_color=color)

def ClearSubframe(subframe: ctk.CTkFrame):
     for widget in subframe.winfo_children():   # deleting all old widgets in subframe
        widget.destroy()

def BrowseAction(file_types:tuple[str,str], entry:ctk.CTkEntry, logger:logging.Logger):
        filename = filedialog.askopenfilename(filetypes=[file_types])
        #filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0,filename)
        entry.configure(state="readonly")
        logger.info(f"Selected file: {filename}")

def ValidateDate(date:str, logger:logging.Logger)->list:
        if not len(date.split('.'))==3:
            return [False, None, None, None]
        dd, mm, yyyy = date.split('.')
        if not dd.isdigit() or not 0 < int(dd) <= 31:
            logger.warning(f'Error with dd: {dd}')
            return [False, None, None, None]
        elif not mm.isdigit() or not 0 < int(mm) <= 12:
            logger.warning(f'Error with mm: {mm}')
            return [False, None, None, None]
        elif not yyyy.isdigit() or not 2024 < int(yyyy) < 2100:
            logger.warning(f'Error with yyyy: {yyyy}')
            return [False, None, None, None]
        else:
            return [True, int(dd), int(mm), int(yyyy)]
        
def DelOldFile(dir:str, file_type:str, logger: logging.Logger):
    #get path to old existing .csv file and delete it
    fpath: Path
    fpaths: list = glob.glob(f"{dir}/*.{file_type}")
    if(len(fpaths) == 0): logger.warning(f"No old .{file_type} file found!")
    elif(len(fpaths) > 1):    # this is unexpected and schould ony happen if there is a bug
        logger.critical(f"Found {len(fpaths)} .{file_type} files, there has to be only one!")
        try:
            for pathstr in fpaths:
                logger.critical(f"Erasing {pathstr}")
                delpath = Path(pathstr)
                delpath.unlink()
        except Exception as e:
            logger.critical(f"Failed to delete old txt file {pathstr}")
            logger.exception(e)
            raise
    else:
        fpath = Path(fpaths[0])
        try:
            fpath.unlink()
            logger.info(f"Deleted old .{file_type} file {fpath}!")
        except Exception as e:
            logger.critical(f"Failed to delete old .{file_type} file {fpath}")
            logger.exception(e)
            raise

def CopyAndRename(srcname: str, dstname: str):
    dest_dir = Path.home() / "Downloads"
    srcfile = f"data/{srcname}"
    copy(srcfile, dest_dir)

    if not settings.cours_name: settings.cours_name = "predmet"
    if not settings.cours_number: settings.cours_number = "smjer"
    if not settings.acad_year: settings.acad_year = "yyyy/yy"

    acad_year1, acad_year2 = str.split(settings.acad_year,'/',1)
    
    new_name = f"{dest_dir}/{settings.cours_name}-{settings.cours_number}-{acad_year1}_{acad_year2}-{dstname}.xlsx"
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