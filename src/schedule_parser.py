class Group:
    def __init__(self, number, day,time,lab):
        self.number = number
        self.day = day
        self.time = time
        self.lab = lab

    def __str__(self):
        return f"{self.number}, {self.day}, {self.time}, {self.lab}"


def pars_schedule_file():
    groups = []
    try:
        with open('../data/schedule.txt',"r") as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                split_line = line.split(",")
                if(len(split_line)==4):
                    groups.append(Group(split_line[0], split_line[1], split_line[2], split_line[3]))
        return groups
    except FileNotFoundError:
        print("The file 'data/schedule.txt' was not found.")
        return
    except IOError:
        print('Error opening schedule file!')
        return
    
    
