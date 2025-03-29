import datetime
class Group:
    def __init__(self, group_label, day, time, lab, group_size):
        self.group_label: str = group_label
        self.day: str = day
        self.time: str = time
        self.lab: str = lab
        self.group_size: int = int(group_size)
        starttime, endtime = time.split("-",1)
        starttime_h,starttime_m = starttime.split(":",1)
        self.starttime: datetime = datetime.time(hour=int(starttime_h), minute=int(starttime_m))
        endtime_h,endtime_m = endtime.split(":",1)
        self.endtime: datetime = datetime.time(hour=int(endtime_h), minute=int(endtime_m))
        
    def __str__(self):
        return f"{self.group_label}, {self.day}, {self.time}, {self.lab}, {self.group_size}"


def pars_schedule_file():
    groups: dict[str, list:Group] = {}
    try:
        with open('data/schedule.txt',"r") as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                split_line = line.split(",")
                #Every line contains: group_label, day, time, lab, group_size
                if(len(split_line)==5):
                    group = Group(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4])
                    if not group.day in groups:
                            groups[group.day] = []
                    groups[group.day].append(group)
        if(len(groups)==0):
            print('Error: Failed to finde groups in \'data/schedule.txt!\'')
            return
        return groups
    except FileNotFoundError:
        print("The file 'data/schedule.txt' was not found.")
        return
    except IOError:
        print('Error opening schedule file!')
        return