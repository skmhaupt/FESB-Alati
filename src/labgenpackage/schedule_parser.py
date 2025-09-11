from labgenpackage.classes import Student
import logging, datetime, csv, os

def schedule_parser(cours_participants: dict[str, Student],src_dir:str) -> tuple[list[Student],list[Student]]:
    logger = logging.getLogger("my_app.schedule_parser")

    logger.info("Parsing .csv files containing schedules!")
    
    fpaths:list = []
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            src_file_path = os.path.join(src_dir, filename)
            fpaths.append(src_file_path)
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




def schedule_parser_2(cours_participants: dict[str, Student],src_dir:str) -> tuple[list[Student],list[Student]]:
    logger = logging.getLogger("my_app.schedule_parser")

    logger.info("Parsing .csv files containing schedules!")
    
    fpaths:list = []
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            src_file_path = os.path.join(src_dir, filename)
            fpaths.append(src_file_path)
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
    

    fpath: str
    for fpath in fpaths:
        #open csv file
        print(fpath)
        try:
            schedule:dict[str, list[tuple]] = {}
            user: str = fpath.split("\\",1)[1].split("_",1)[0]
            csvUserNames.append(user)
            if(user in cours_participants):
                #logger.debug(f"Found student: {cours_participants[user]}")
                if os.path.getsize(fpath) == 0:
                    cours_participants[user].schedule = schedule
                    raise ValueError
                print("-----------------------------------------------------------------")
                print(f"Student: {cours_participants[user]}")
                with open(fpath, newline='', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    #skip first line
                    next(reader)
                    #Every row contains: id, name, shortName, colorId, professor, eventType, groups, classroom, start, end, description, recurring, recurringType, recurringUntil, studyCode
                    #                    0   1     2          3        4          5          6       7          8      9    10           11         12             13              14
                    for row in reader:
                        #row[10]: day dd.mm.yyyy hh:mm - hh:mm (3 sata)
                        _, date, time = row[10].split(" ", 2)
                        dd,mm,yyyy,_ = date.split(".",3)
                        time,_ = time.split("(",1)
                        time = time.strip()
                        starttime, endtime = time.split(" - ",1)
                        h,m = starttime.split(":",1)
                        appointment_start = datetime.datetime(year=int(yyyy), month=int(mm), day=int(dd), hour=int(h), minute=int(m))
                        h,m = endtime.split(":",1)
                        appointment_end = datetime.datetime(year=int(yyyy), month=int(mm), day=int(dd), hour=int(h), minute=int(m))
                        
                        date = appointment_start.date()
                        date = f"{date}"
                        if not date in schedule.keys():
                            schedule[date] = []
                        schedule[date].append((appointment_start, appointment_end))
                        print(f"{date} = Start: {appointment_start} End: {appointment_end}")

                    cours_participants[user].schedule = schedule
            else:
                logger.error(f"Found .csv for user {user}, but the user is not in cours_participants!")
                csvErrors.append(user)
        except ValueError as e:
            logger.exception(e)
            logger.warning(f"csv file for student {user} is empty.")
            csvEmpty.append(cours_participants[user])
        except Exception as e:
            logger.critical(f"Error with parsing a csv file for user: {user}")
            logger.exception(e)
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