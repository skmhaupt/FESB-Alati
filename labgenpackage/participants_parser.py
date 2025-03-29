import csv
import glob

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
        self.groups: list = []

    def __str__(self):
        return f"{self.fullname}({self.jmbag}), Username: {self.username}, E-Mail: {self.email}"

def pars_cours_participants() -> dict[str, Student]:
    cours_participants: dict[str, Student] = {}
    
    #get path to file
    fpath: str
    fpaths: list = glob.glob('data/courseid_*_participants.csv')
    if(len(fpaths) > 1):
        print('Error: Found', len(fpaths), 'courseid_#number_participants.csv files, make sure there is only one!')
        return
    elif(len(fpaths) == 0):
        print('Error: No courseid_#number_participants.csv file found!')
        return
    fpath = fpaths[0]

    #open csv file
    try:
        with open(fpath, newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            #skip first line
            next(reader)
            #Every row contains: ime, prezime, email, jmbag
            for row in reader:
                student: Student = Student(row[0],row[1],row[2],row[3])
                cours_participants[student.username] = student
        return cours_participants
    except IOError:
        print('Error with csv file', IOError)
        return
