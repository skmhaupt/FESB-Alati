import customtkinter as ctk
import gui.settings as settings
import re, json, logging

# This frame has no special function, its contents are used by other sections. The user doesnt have to fill out its data.
class CoursFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.v_year = (self.register(self.year_callback))

        self.label_1 = ctk.CTkLabel(self, text='Predmet:')
        self.label_1.grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')
        self.cours_name_entry = ctk.CTkEntry(self, placeholder_text='npr: PDS, SDOS, itd.')
        self.cours_name_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='e')

        self.label_2 = ctk.CTkLabel(self, text='Smjer:')
        self.label_2.grid(row=0, column=2, padx=(10, 5), pady=10, sticky='w')
        self.cours_number_entry = ctk.CTkEntry(self, placeholder_text='npr: 112, 222 itd.')
        self.cours_number_entry.grid(row=0, column=3, padx=(0, 10), pady=10, sticky='e')

        self.label_3 = ctk.CTkLabel(self, text='Akademska godina:')
        self.label_3.grid(row=0, column=4, padx=(10, 5), pady=10, sticky='w')
        self.year_entry = ctk.CTkEntry(self, validate='all', validatecommand=(self.v_year, '%P'))
        self.year_entry.grid(row=0, column=5, padx=(0, 10), pady=10, sticky='e')
        self.year_entry.configure(placeholder_text='npr: yyyy/yy')

        if not settings.cours_name=='':
            self.cours_name_entry.insert(0,settings.cours_name)
        if not settings.cours_number=='':
            self.cours_number_entry.insert(0,settings.cours_number)
        if not settings.acad_year=='':
            self.year_entry.insert(0,settings.acad_year)
        
    def year_callback(self, P):
        if P == 'npr: yyyy/yy': return True
        if re.fullmatch('[0-9]{0,3}', P): return True
        elif re.fullmatch('[0-9]{4}', P):
            year2 = int(P[-2:])+1
            self.year_entry.after(1, lambda: self.year_entry.insert(4,f'/{year2:02d}'))
            return True
        elif len(P)==6:
            self.year_entry.after(1, lambda: self.year_entry.delete(3,ctk.END))
            return True
        elif re.fullmatch('[0-9]{4}/[0-9]{2}', P): 
            return True
        else: return False
    
    def get_data(self):
        settings.cours_name = self.cours_name_entry.get()
        settings.cours_number = self.cours_number_entry.get()
        settings.acad_year = self.year_entry.get()
    
    def set_entries(self):
        self.cours_name_entry.delete(0, 'end')
        self.cours_name_entry.insert(0,settings.cours_name)
        self.cours_number_entry.delete(0, 'end')
        self.cours_number_entry.insert(0,settings.cours_number)
        self.year_entry.delete(0, 'end')
        self.year_entry.insert(0,settings.acad_year)


    
    def save_data(self):
        logger = logging.getLogger('my_app.coursframe')

        settings.cours_name = self.cours_name_entry.get()
        settings.cours_number = self.cours_number_entry.get()
        settings.acad_year = self.year_entry.get()

        with open("data/data.json", "r") as file:
            data:dict[str:str] = json.load(file)
        data["cours"] = settings.cours_name
        data["cours_number"] = settings.cours_number
        data["acad_year"] = settings.acad_year
        json_object = json.dumps(data, indent=4)
        logger.info(f"Saving cours data: {settings.cours_name} - {settings.cours_number}; {settings.acad_year}")
        with open("data/data.json", "w") as file:
            file.write(json_object)