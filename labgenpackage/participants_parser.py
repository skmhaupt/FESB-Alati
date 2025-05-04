from labgenpackage.classes import Student
import csv
import glob
import logging

def pars_cours_participants() -> tuple[dict[str, Student], str]:
    
    logger = logging.getLogger("my_app.participants_parsere")

    cours_participants: dict[str, Student] = {}
    
    #get path to file
    fpath: str
    fpaths: list = glob.glob("data/*.csv")
    if(len(fpaths) > 1):
        logger.critical(f"Found {len(fpaths)} .csv files, there can only be one!")
        raise FileNotFoundError
        #return
    elif(len(fpaths) == 0):
        logger.error("No .csv file found!")
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
        return (cours_participants, fpath)
    except Exception:
        logger.critical('Error with csv file!')
        raise