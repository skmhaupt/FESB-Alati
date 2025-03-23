import csv
import glob

class Student:
    def __init__(self, name, surname,email,jmbag):
        self.name = name
        self.surname = surname
        self.fullname = surname + " " + name
        self.email = email
        self.username,_ = email.split("@",1)
        self.jmbag = jmbag

    def __str__(self):
        return f"{self.fullname}({self.jmbag}), Username: {self.username}, E-Mail: {self.email}"

def pars_cours_participants():
    cours_participants = []
    
    #get path to file
    fpath = glob.glob('../data/courseid_*_participants.csv')
    if(len(fpath) > 1):
        print('Error: Found', len(fpath), 'courseid_#number_participants.csv files, make sure there is only one!')
        return
    elif(len(fpath) == 0):
        print('Error: No courseid_#number_participants.csv file found!')
        return
    fpath = fpath[0]

    #open csv file
    try:
        with open(fpath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            #skip first line
            next(reader)
            #Every row contains: ime, prezime, email, jmbag
            for row in reader:
                cours_participants.append(Student(row[0],row[1],row[2],row[3]))
        return cours_participants
    except IOError:
        print('Error with csv file', IOError)
        return