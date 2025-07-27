import datetime
import logging

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38m"
    yellow = "\x1b[33m"
    red = "\x1b[31;4m"
    bold_red = "\x1b[31;4;1m"
    reset = "\x1b[0m"
    format = "{asctime} - {name:<11} - {levelname}\t- {message} ({filename}:{lineno})"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,style="{")
        return formatter.format(record)

class Group:
    def __init__(self, group_label:str, day:str, time:str, lab:str, group_size:int):
        self.group_label: str = group_label
        self.day: str = day
        self.time: str = time
        self.lab: str = lab
        self.group_size: int = int(group_size)
        self.students: list[Student] = []
        if not time=="NaN":
            starttime, endtime = time.split("-",1)
            starttime_h,starttime_m = starttime.split(":",1)
            self.starttime: datetime = datetime.time(hour=int(starttime_h), minute=int(starttime_m))
            endtime_h,endtime_m = endtime.split(":",1)
            self.endtime: datetime = datetime.time(hour=int(endtime_h), minute=int(endtime_m))
        
    def __str__(self):
        #Fix time string
        if self.time=="NaN":
            time = "NaN"
        else:
            time = self.time.replace(' ', '')
            a,b = self.time.split("-")
            time = f"{a} - {b}"
        return f"{self.group_label} - {self.day} {time} ({self.lab})"
    
    def __repr__(self):
        return f"{self.group_label}"

class Student:
    def __init__(self, name: str, surname: str,email: str,jmbag: str):
        #student data
        self.name: str = name
        self.surname: str = surname
        self.fullname: str = surname + " " + name
        self.email: str = email
        self.username,_ = email.split("@",1)
        self.jmbag: int = int(jmbag)
        self.schedule: dict[str, list] = {}
        #data for sorting
        self.total_places: int = 0      #total places provided by groups
        self.weight: int = 0            #weight based on total places
        self.norm_weight: float = 0     #weight/total_places
        self.position: int = 0          #position amongst students based on alfabetical order
        self.norm_alf_weight: float = 0 #normalised alfabetical weight = position/total_num_of_students
        self.variable_weight: float = 0 #variable_weight = norm_weight*(100-alf_prio_lvl) + norm_alf_weight*alf_prio_lvl
        self.alf_prio_lvl: int = 0      #defines the priority level for alfabetical sorting
        self.groups: list[Group] = []   #all groups the student can be assigned to
        self.group: Group               #the group the student has been assigned to

    def __str__(self):
        return f"{self.fullname}({self.jmbag}), Username: {self.username}, E-Mail: {self.email}"
    
    def __repr__(self):
        return f"{self.fullname}"
    
    def update_weight(self):
        weight: int = 0
        group: Group
        for group in self.groups:
            weight += group.group_size
        self.weight = weight
        self.norm_weight = self.weight / self.total_places
    
    def set_group(self, group: Group):
        self.group = group
    
    def set_alf_weight(self, total_num_of_students):
        self.norm_alf_weight = self.position / total_num_of_students
    
    def set_group_weight(self, total_places:int):
        self.total_places = total_places
        self.norm_weight = self.weight / total_places
    
    def set_var_weight(self, alf_prio_lvl: int):
        self.alf_prio_lvl = alf_prio_lvl
        self.variable_weight = (self.norm_weight * (100-self.alf_prio_lvl)) + (self.norm_alf_weight * self.alf_prio_lvl)

    def update_var_weight(self):
        self.variable_weight = (self.norm_weight * (100-self.alf_prio_lvl)) + (self.norm_alf_weight * self.alf_prio_lvl)