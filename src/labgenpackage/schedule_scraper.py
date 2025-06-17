import os, subprocess, datetime, glob, csv, logging
from subprocess import PIPE, STDOUT
from pathlib import Path
from labgenpackage.classes import Student

def log_subprocess_output(pipe, logger: logging):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logger.info('got line from subprocess: %r', line)

def schedule_scraper(cours_participants: dict[str, Student], scraper_state:bool, startdate:str="", enddate:str="") -> tuple[list[Student],list[Student]]:

    logger = logging.getLogger("my_app.schedule_scraper")
    logger.setLevel("INFO")

    if scraper_state:
        try:
            os.chdir('Raspored_scraping')
            logger.info(f"Now in {os.getcwd()} directory!")
        except Exception:
            logger.critical("Failed to enter /Raspored_scraping directory.")
            raise

        logger.info("Creating/opening dates.txt file for Raspored_scraping.")
        try:
            dates_file = open("data/dates.txt", "w")

            dates_file.write(f"{startdate}\n")
            dates_file.write(f"{enddate}\n")
            dates_file.close()
        except Exception:
            logger.critical("Failed with dates.txt.")
            raise
        
        logger.info("Creating usernames.txt file for Raspored_scraping.")
        try:
            usernames_file = open("data/usernames.txt", "w")
            student: Student
            if cours_participants:
                for student in cours_participants.values():
                    usernames_file.write(f"{student.username}\n")
                usernames_file.close()
        except Exception:
            logger.critical("Failed with usernames.txt.")
            raise

        if not cours_participants:
            logger.error("Coursparticipants not loaded.")
            try:
                os.chdir('..')
                logger.info(f"Now in {os.getcwd()} directory!\n")
            except Exception:
                logger.critical("Failed to exit /Raspored_scraping directory.")
                raise
            raise FileNotFoundError
        
        logger.info("Deleting old data from data/timetables!")
        try:
            folder =  Path("data/timetables")
            for item in folder.rglob("*"):
                item.unlink()
        except Exception:
            logger.critical(f"Failed to delete {item}")
            os.chdir('..')
            logger.info(f"Now in {os.getcwd()} directory!\n")
            raise

        logger.info("Launching schedule scraper!")
        try:
            #subprocess.run(['.\\gradlew', 'run'], shell=True, check=True)
            pro = subprocess.Popen('.\\gradlew run --no-daemon', shell=True, stdout=PIPE, stderr=STDOUT) #, preexec_fn=os.setsid
            with pro.stdout:
                log_subprocess_output(pro.stdout, logger)
            pro.wait()
        except subprocess.CalledProcessError:
            #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            logger.critical("Error with running subprocess /gradlew")
            os.chdir('..')
            logger.info(f"Now in {os.getcwd()} directory!\n")
            raise

        os.chdir('..')
        logger.info(f"Now in {os.getcwd()} directory!\n")

    else:
        logger.info("Variable scraper_state set to off, skiping schedule scraper!")


    logger.info("Parsing .csv files containing schedules!")
    fpaths: list = glob.glob('Raspored_scraping/data/timetables/*.csv')
    if(len(fpaths) > 1):
        logger.info(f"Found {len(fpaths)} .csv files.")
    elif(len(fpaths) == 0):
        logger.error("No .csv files found in Raspored_scraping/data/timetables/!")
        raise FileNotFoundError
    
 
    
    Errors:list[Student] = []
    csvErrors:list[Student] = []
    csvMissing:list[Student] = []
    csvEmpty:list[Student] = []
    csvUserNames:list[str]=[]
    days = {
        "ponedjeljak": "PON",
        "utorak": "UTO",
        "srijeda": "SRI",
        "četvrtak": "ČET",
        "petak": "PET"
    }

    fpath: str
    for fpath in fpaths:
        #open csv file
        try:
            tempschedule:dict[str, set] = {}
            schedule:dict[str, list] = {
                "PON": [],
                "UTO": [],
                "SRI": [],
                "ČET": [],
                "PET": []
            }
            user: str = fpath.split("\\",1)[1].split("_",1)[0]
            csvUserNames.append(user)
            if(user in cours_participants):
                #logger.debug(f"Found student: {cours_participants[user]}")
                if os.path.getsize(fpath) == 0:
                    cours_participants[user].schedule = schedule
                    raise ValueError
                with open(fpath, newline='', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    #skip first line
                    next(reader)
                    #Every row contains: id, name, shortName, colorId, professor, eventType, groups, classroom, start, end, description, recurring, recurringType, recurringUntil, studyCode
                    #                    0   1     2          3        4          5          6       7          8      9    10           11         12             13              14
                    for row in reader:
                        #row[10]: day date hh:mm - hh:mm (3 sata)
                        day, _, time = row[10].split(" ", 2)
                        time,_ = time.split("(",1)
                        time = time.strip()
                        if not day in tempschedule:
                            tempschedule[day] = set()
                        tempschedule[day].add(time)
                    for day in tempschedule:
                        #logger.debug(f"{day}: {tempschedule[day]}")
                        for time in tempschedule[day]:
                            #logger.debug(f"{time}")
                            starttime, endtime = time.split(" - ",1)
                            starttime_h,starttime_m = starttime.split(":",1)
                            starttime = datetime.time(hour=int(starttime_h), minute=int(starttime_m))
                            endtime_h,endtime_m = endtime.split(":",1)
                            endtime = datetime.time(hour=int(endtime_h), minute=int(endtime_m))
                            #schedule[days[day]].insert(len(schedule), [starttime,endtime])
                            schedule[days[day]].append([starttime,endtime])
                            #print("starttime:", starttime, "endtime:", endtime)
                        #print(day, ": ",schedule[days[day]])
                    #print("----------------------------\n")
                    cours_participants[user].schedule = schedule
            else:
                logger.error(f"Found .csv for user {user}, but the user is not in cours_participants!")
                csvErrors.append(user)
        except ValueError:
            logger.warning(f"csv file for student {user} is empty.")
            csvEmpty.append(cours_participants[user])
        except Exception:
            logger.critical(f"Error with parsing a csv file for user: {user}")
            Errors.append(cours_participants[user])
            #logger.critical(f"test {Errors}")
            #logger.warning(f"Removing {user} from list. He will not be added to a group!")
            #cours_participants.pop(user)
    
    for user in cours_participants:
        if user not in csvUserNames:
            logger.warning(f"csv file missing for student: {cours_participants[user]}")
            csvMissing.append(cours_participants[user])

    if Errors:
        logger.error(f"Errors with users: {Errors}")
        raise Exception(Errors)
    if csvErrors:
        logger.error(f"Users and .csv files in 'data/timetables/' are out of sync. Found following .csv files that dont have a user: {*csvErrors,}")
        raise ValueError
    if csvMissing:
        logger.warning(f"Students missing csv files: {*csvMissing,}")
    if csvEmpty:
        logger.warning(f"Students with empty csv files: {*csvEmpty,}")
    
    return (csvMissing, csvEmpty)