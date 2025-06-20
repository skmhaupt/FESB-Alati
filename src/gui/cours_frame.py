import customtkinter as ctk

# This frame has no special function, its contents are used by other sections. The user doesnt have to fill out its data.
class CoursFrame(ctk.CTkFrame):
    def __init__(self, master, cours_name, cours_number):
        super().__init__(master)
        self.label_1 = ctk.CTkLabel(self, text="Predmet:")
        self.label_1.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="w")
        self.cours_name_entry = ctk.CTkEntry(self, placeholder_text="npr: PDS, SDOS, itd.")
        self.cours_name_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="e")

        self.label_2 = ctk.CTkLabel(self, text="Smjer:")
        self.label_2.grid(row=0, column=2, padx=(10, 5), pady=(10, 10), sticky="w")
        self.cours_number_entry = ctk.CTkEntry(self, placeholder_text="npr: 112, 222 itd.")
        self.cours_number_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10), sticky="e")

        if not cours_name=="":
            self.cours_name_entry.insert(0,cours_name)
        if not cours_number=="":
            self.cours_number_entry.insert(0,cours_number)