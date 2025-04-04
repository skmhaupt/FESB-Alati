import os, subprocess, datetime, glob, csv
from pathlib import Path
from labgenpackage.classes import Student

def schedule_scraper(cours_participants: dict[str, Student], scraper_state:bool):
    if scraper_state:
        date = datetime.datetime.now()
        #summer_semester_start_date = datetime.datetime(date.year, 2, 24)
        #winter_semester_start_date = datetime.datetime(date.year, 10, 1)
        os.chdir('Raspored_scraping')
        print('Now in', os.getcwd(), 'directory!')
    
        print('Creating dates.txt file for Raspored_scraping.')
        dates_file = open("data/dates.txt", "w")
    
        # Put here the start and end date of the period you want to check in the format DD-MM-YYYY
        if date.month<10 and date.month>=2:
            print("In summer semester!")
            dates_file.write(f"01-03-{date.year}\n")
            dates_file.write(f"24-04-{date.year}")
        else:
            print("In winter semester!")
            dates_file.write(f"01-10-{date.year}\n")
            dates_file.write(f"15-12-{date.year}")
        dates_file.close()

        print('Creating usernames.txt file for Raspored_scraping.')
        usernames_file = open("data/usernames.txt", "w")
        student: Student
        for student in cours_participants.values():
            usernames_file.write(f"{student.username}\n")
        usernames_file.close()

        print("Deleting old data from data/timetables!")
        folder =  Path("/data/timetables")
        for item in folder.rglob("*"):
            try:
                item.unlink()
            except OSError as e:
                print(f"Failed to delete {item}. {e}")
                raise

        print("Launching schedule scraper!")
        subprocess.run(['.\\gradlew', 'run'], shell=True)

        os.chdir('..')
        print('Now in', os.getcwd(), 'directory!\n')

    else:
        print("Variable scraper_state set to off, skiping schedule scraper!")


    print("Parsing .csv files containing schedules!")
    fpaths: list = glob.glob('Raspored_scraping/data/timetables/*.csv')
    if(len(fpaths) > 1):
        print('Found', len(fpaths), '.csv files.')
    elif(len(fpaths) == 0):
        print('Error: No .csv files found!')
        return
    
    Errors: list = []
    nocsvError:list = []
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
            if(user in cours_participants):
                #print("Found student: ", cours_participants[user])
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
                        #print(day, ": ",tempschedule[day])
                        for time in tempschedule[day]:
                            #print(time)
                            starttime, endtime = time.split(" - ",1)
                            starttime_h,starttime_m = starttime.split(":",1)
                            starttime = datetime.time(hour=int(starttime_h), minute=int(starttime_m))
                            endtime_h,endtime_m = endtime.split(":",1)
                            endtime = datetime.time(hour=int(endtime_h), minute=int(endtime_m))
                            #schedule[days[day]].insert(len(schedule), [starttime,endtime])
                            schedule[days[day]].append([starttime,endtime])
                            #print("starttime:", starttime, "endtime:", endtime)
                        #print(day, ": ",schedule[days[day]])
                    #print(schedule)
                    #print("----------------------------\n")
                    cours_participants[user].schedule = schedule
            else:
                nocsvError.append(user)
        except Exception as e:
            print('Error with csv file', e)
            Errors.append(user)
            print("Removing", user, "from list. He will not be added to a group!")
            cours_participants.pop(user)
    if Errors or nocsvError:            
        print("Errors with users: ", Errors, "\n")
        print(".csv file mising for users: ", nocsvError, "\n")
