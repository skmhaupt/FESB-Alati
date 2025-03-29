import csv
import glob

class Student:
    def __init__(self, name: str, surname: str,email: str,jmbag: str):
        self.name = name
        self.surname = surname
        self.fullname = surname + " " + name
        self.email = email
        self.username,_ = email.split("@",1)
        self.jmbag = jmbag
        self.schedule: dict[str, list] = {}
        self.weight: int = 0
        self.groups: list = []

    def __str__(self):
        return f"{self.fullname}({self.jmbag}), Username: {self.username}, E-Mail: {self.email}"

def pars_cours_participants():
    cours_participants:dict[str, Student] = {}
    
    #get path to file
    fpath = glob.glob('data/courseid_*_participants.csv')
    if(len(fpath) > 1):
        print('Error: Found', len(fpath), 'courseid_#number_participants.csv files, make sure there is only one!')
        return
    elif(len(fpath) == 0):
        print('Error: No courseid_#number_participants.csv file found!')
        return
    fpath = fpath[0]

    #open csv file
    try:
        with open(fpath, newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            #skip first line
            next(reader)
            #Every row contains: ime, prezime, email, jmbag
            for row in reader:
                student = Student(row[0],row[1],row[2],row[3])
                cours_participants[student.username] = student
        return cours_participants
    except IOError:
        print('Error with csv file', IOError)
        return
