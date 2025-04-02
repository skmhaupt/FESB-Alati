import datetime

class Group:
    def __init__(self, group_label, day, time, lab, group_size):
        self.group_label: str = group_label
        self.day: str = day
        self.time: str = time
        self.lab: str = lab
        self.group_size: int = int(group_size)
        self.students: list[Student] = []
        starttime, endtime = time.split("-",1)
        starttime_h,starttime_m = starttime.split(":",1)
        self.starttime: datetime = datetime.time(hour=int(starttime_h), minute=int(starttime_m))
        endtime_h,endtime_m = endtime.split(":",1)
        self.endtime: datetime = datetime.time(hour=int(endtime_h), minute=int(endtime_m))
        
    def __str__(self):
        return f"{self.group_label}, {self.day}, {self.time}, {self.lab}, {self.group_size}"


class Student:
    def __init__(self, name: str, surname: str,email: str,jmbag: str):
        self.name: str = name
        self.surname: str = surname
        self.fullname: str = surname + " " + name
        self.email: str = email
        self.username,_ = email.split("@",1)
        self.jmbag: int = int(jmbag)
        self.schedule: dict[str, list] = {}
        self.weight: int = 0
        self.groups: list[Group] = []

    def __str__(self):
        return f"{self.fullname}({self.jmbag}), Username: {self.username}, E-Mail: {self.email}"
    
    def set_weight(self):
        weight: int = 0
        group: Group
        for group in self.groups:
            weight += group.group_size
        self.weight = weight