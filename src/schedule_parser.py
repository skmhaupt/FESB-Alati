class Group:
    def __init__(self, group_number, day, time, lab, group_size):
        self.group_number = group_number
        self.day = day
        self.time = time
        self.lab = lab
        self.group_size = group_size

    def __str__(self):
        return f"{self.group_number}, {self.day}, {self.time}, {self.lab}, {self.group_size}"


def pars_schedule_file():
    groups = []
    try:
        with open('data/schedule.txt',"r") as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                split_line = line.split(",")
                #Every line contains: group_number, day, time, lab, group_size
                if(len(split_line)==5):
                    groups.append(Group(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4]))
        
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