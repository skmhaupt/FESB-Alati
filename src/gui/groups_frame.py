from labgenpackage.schedule_parser import pars_schedule_file
from labgenpackage.classes import Group
from customtkinter import filedialog
from pathlib import Path
from shutil import copy

import customtkinter as ctk
import gui.settings as settings
import logging, glob

# GroupFrame crates the section used for uploading a group.txt file.
# The only function that is used from the main program is 'pars_schedule_file', and while a
# 'group' variable is created it is only used in this section to display data that will be
# loaded in the main section 'Fill_groups' later on.

class GroupsFrame(ctk.CTkFrame):
    def __init__(self, master, logger: logging.Logger):
        super().__init__(master)

        self.logger = logger

        self.controller = master    #in case ctk widgets from other sections have to be accessed

        self.grid_columnconfigure(1, weight=1)  #column 1 is flex
        self.grid_rowconfigure(6, weight=1)     #rwo 6 is flex, subframe is in row 6 and it displays all the loaded groups

        self.section_title_label = ctk.CTkLabel(self, text="Grupe", font=("Helvetica", 23))
        self.section_title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="we")

        self.entry_label = ctk.CTkLabel(self, text="Ulazna datoteka:")
        self.entry_label.grid(row=1, column=0, padx=(10,5), pady=(10, 0), sticky="we")

        self.txt_file_entry = ctk.CTkEntry(self, width=100, placeholder_text=".txt datoteka")   #this widget will containe the path to the .txt file
        self.txt_file_entry.configure(state="readonly")
        self.txt_file_entry.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0, 0), sticky="we")

        self.browse_button = ctk.CTkButton(self,width=60 , text="Pretrazi", command=self.BrowseAction)  #button to get path to .txt file
        self.browse_button.grid(row=2, column=2, padx=(0, 10), pady=(0, 0), sticky="we")

        self.upload_button = ctk.CTkButton(self,width=125 , text="Ucitaj datoteku", command=self.UploadAction)  #button to load the selected .txt file
        self.upload_button.grid(row=3, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="")

        #widgets to display summary of loaded data
        self.loaded_schedule_label = ctk.CTkLabel(self, text="Nije ucitan raspored grupa.")
        self.loaded_schedule_label.grid(row=4, column=0,columnspan=3, padx=(10,0), pady=(10, 0), sticky="")
        self.num_of_groups_label = ctk.CTkLabel(self, text="Broj grupa: N/A")
        self.num_of_groups_label.grid(row=5, column=0, padx=(10,0), pady=0, sticky="")
        self.num_of_places_label = ctk.CTkLabel(self, text="Broj dostupnih mjesta: N/A")
        self.num_of_places_label.grid(row=5, column=1, columnspan=2, padx=(0,20), pady=0, sticky="")

        #subframe that will display loaded groups and errors
        self.subframe = ctk.CTkScrollableFrame(self)
        self.subframe.grid(row=6, column=0, columnspan=3, padx=10, pady=(0,10),sticky="wens")
        self.default_subframe_label = ctk.CTkLabel(self.subframe, text="Grupe nisu ucitane.")
        self.default_subframe_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="we")

        #load data from old session on startup
        try:
            self.LoadGroups()
        except FileNotFoundError:
            return
        except Exception:
            self.logger.error("Error when loading groups on startup!")
            return
    
    def LoadGroups(self)->str:
        #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
        settings.loaded_data[0] = False

        try:
            groups, filename = pars_schedule_file()
        except ValueError:
            self.NoGroupsInUploadedFile()
            return
        except FileNotFoundError:
            raise
        except Exception:
            self.logger.error("Failed parcing participants!")
            raise

        for widget in self.subframe.winfo_children():
            widget.destroy()  # deleting widget

        row:int = 2
        
        group:Group
        for groups_in_day in groups.values():
            for group in groups_in_day:
                self.AddGrouplabel(row,group)
                settings.total_places+=group.group_size
                row+=1
        self.logger.info(f"Found {row-2} groups. With {settings.total_places} places in total.")
        
        self.loaded_schedule_label.configure(text=f"Ucitani raspored: {filename}")
        self.num_of_groups_label.configure(text=f"Broj grupa: {row-2}")
        self.num_of_places_label.configure(text=f"Broj dostupnih mjesat: {settings.total_places}")
        settings.loaded_data[0] = True

    
    def NoGroupsInUploadedFile(self):
        self.loaded_schedule_label.configure(text=f"Nije ucitan raspored grupa.")
        self.num_of_groups_label.configure(text=f"Broj grupa: N/A")
        self.num_of_places_label.configure(text=f"Broj dostupnih mjesta: N/A")

        for widget in self.subframe.winfo_children():
            widget.destroy()  # deleting widget

        self.warning_label = ctk.CTkLabel(self.subframe, text=f"Ispravni format zapisa grupa u datoteci:", text_color="red")
        self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label2 = ctk.CTkLabel(self.subframe, text=f"grupa, dan, od - do, dvorana, broj studenta")
        self.warning_label2.grid(row=3, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label3 = ctk.CTkLabel(self.subframe, text=f"G1, PON, 09:30 - 11:00, B419, 12")
        self.warning_label3.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label4 = ctk.CTkLabel(self.subframe, text=f"G2, UTO, 09:30 - 11:00, B419, 12")
        self.warning_label4.grid(row=5, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label5 = ctk.CTkLabel(self.subframe, text=f"GC, SRI, 09:30 - 11:00, B419, 12")
        self.warning_label5.grid(row=6, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label6 = ctk.CTkLabel(self.subframe, text=f"GD, ČET, 09:30 - 11:00, B419, 12")
        self.warning_label6.grid(row=7, column=0, padx=5, pady=(5, 0), sticky="w")
        self.warning_label7 = ctk.CTkLabel(self.subframe, text=f"Grupa5, PET, 09:30 - 11:00, B419, 12")
        self.warning_label7.grid(row=8, column=0, padx=5, pady=(5, 0), sticky="w")

    def AddGrouplabel(self, row:int, group:Group):
        self.group_label1 = ctk.CTkLabel(self.subframe, text=f"{group.group_label}")
        self.group_label1.grid(row=row, column=0, padx=5, pady=(5, 0), sticky="we")
        self.group_label2 = ctk.CTkLabel(self.subframe, text=f"{group.day}")
        self.group_label2.grid(row=row, column=1, padx=5, pady=(5, 0), sticky="we")
        self.group_label3 = ctk.CTkLabel(self.subframe, text=f"{group.time}")
        self.group_label3.grid(row=row, column=2, padx=5, pady=(5, 0), sticky="we")
        self.group_label4 = ctk.CTkLabel(self.subframe, text=f"{group.lab}")
        self.group_label4.grid(row=row, column=3, padx=5, pady=(5, 0), sticky="we")
        self.group_label5 = ctk.CTkLabel(self.subframe, text=f"{group.group_size}")
        self.group_label5.grid(row=row, column=4, padx=5, pady=(5, 0), sticky="we")

    def BrowseAction(self):
        filename = filedialog.askopenfilename()
        self.txt_file_entry.configure(state="normal")
        self.txt_file_entry.delete(0, "end")
        self.txt_file_entry.insert(0,filename)
        self.txt_file_entry.configure(state="readonly")
        self.logger.info(f"Selected file: {filename}")

    def UploadAction(self):
        settings.loaded_data[0] = False
        global working
        if working:
            self.logger.warning("Already runing another section! Cant upload new groups.")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
            
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Vec je pokrenuta druga sekcija.\nSacekajte dok ne zavrsi sa izvodenjem", text_color="red")
            self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            
            self.loaded_schedule_label.configure(text=f"Nije ucitan raspored grupa.")
            self.num_of_groups_label.configure(text=f"Broj grupa: N/A")
            self.num_of_places_label.configure(text=f"Broj dostupnih mjesta: N/A")
            return
        input_txt_file = self.txt_file_entry.get()
        if(input_txt_file==""):
            self.logger.warning("Select a .txt file befor uploading.")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Nije zadana .txt datoteka.", text_color="red")
            self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return
        elif input_txt_file.endswith(".txt"):
            self.logger.info(f"{self.txt_file_entry.get()}")
        else:
            self.logger.warning("Input file hase to be a .txt file.")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
            self.warning_label = ctk.CTkLabel(self.subframe, text=f"Odabrana pogresna datoteka.", text_color="red")
            self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return
        
        #get path to old existing .txt file
        fpath: Path
        fpaths: list = glob.glob("data/*.txt")
        if(len(fpaths) > 1):
            self.logger.critical(f"Found {len(fpaths)} old .txt files, there has to be only one!")
            self.logger.critical(f"Erasing all \'.txt\' files!")
            for pathstr in fpaths:
                self.logger.critical(f"Erasing {pathstr}")
                delpath = Path(pathstr)
                delpath.unlink()
        elif(len(fpaths) == 0):
            self.logger.info("No old .txt file found!")
        else:
            fpath = Path(fpaths[0])
            try:
                fpath.unlink()
                self.logger.info(f"Deleted old .txt file {fpath}!")
            except Exception:
                self.logger.critical(f"Failed to delete old txt file {fpath}")
                for widget in self.subframe.winfo_children():
                    widget.destroy()  # deleting widget
                    self.warning_label = ctk.CTkLabel(self.subframe, text=f"Neocekivana pogreska.\nPokusajte ponovo.", text_color="red")
                    self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
                return
        
        #get new selected .txt file
        fpath = Path(input_txt_file)
        try:
            copy(fpath, "data/")
            self.logger.info(f"Uploaded new file: {fpath}!")
        except Exception:
            self.logger.critical(f"Failed to copy new file: {fpath}!")
            for widget in self.subframe.winfo_children():
                widget.destroy()  # deleting widget
                self.warning_label = ctk.CTkLabel(self.subframe, text=f"Neocekivana pogreska.\nPokusajte ponovo.", text_color="red")
                self.warning_label.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
            return

        self.LoadGroups()