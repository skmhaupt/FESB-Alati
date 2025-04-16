from labgenpackage.classes import Student
import csv
import glob
import logging

def pars_cours_participants() -> dict[str, Student]:
    
    logger = logging.getLogger("my_app.participants_parsere")

    cours_participants: dict[str, Student] = {}
    
    #get path to file
    fpath: str
    fpaths: list = glob.glob("data/courseid_*_participants.csv")
    if(len(fpaths) > 1):
        logger.error(f"Found {len(fpaths)} courseid_#number_participants.csv files, make sure there is only one!")
        return
    elif(len(fpaths) == 0):
        logger.error("No courseid_#number_participants.csv file found!")
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
    except Exception:
        raise logger.exception('Error with csv file!')