from labgenpackage.classes import Student
import csv
import glob
import logging

def pars_cours_participants() -> tuple[dict[str, Student], str]:
    
    try:
        logger = logging.getLogger("my_app.participants_parsere")
        logger.setLevel("INFO")
        cours_participants: dict[str, Student] = {}
        
        #get path to file
        fpath: str
        fpaths: list = glob.glob("data/*.csv")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} .csv files, there can only be one!")
            raise FileNotFoundError
        elif(len(fpaths) == 0):
            raise FileNotFoundError
        fpath = fpaths[0]

        #open csv file
        with open(fpath, newline='', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            #skip first line
            next(reader)
            #Every row contains: ime, prezime, email, jmbag
            for row in reader:
                if not isinstance(row[0], str) or not isinstance(row[1], str) or "@" not in row[2] or not row[3].isnumeric():
                    raise ValueError(fpath)
                student: Student = Student(row[0],row[1],row[2],row[3])
                cours_participants[student.username] = student
        return (cours_participants, fpath)
    
    except FileNotFoundError:
        logger.warning("No .csv file found when parsing cours participants!")
        raise
    except ValueError:
        logger.warning("Wrong data in .csv file!")
        raise
    except Exception:
        logger.critical('Error with csv file!')
        raise