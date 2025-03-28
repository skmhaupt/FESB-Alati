import os
import subprocess
import datetime
import glob
import csv
from labgenpackage.participants_parser import Student

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
        for student in cours_participants.values():
            usernames_file.write(f"{student.username}\n")
        usernames_file.close()

        print("Launching schedule scraper!")
        subprocess.run(['.\\gradlew', 'run'], shell=True)

        os.chdir('..')
        print('Now in', os.getcwd(), 'directory!\n')

    else:
        print("Variable scraper_state set to off, skiping schedule scraper!")


    print("Parsing .csv files containing schedules!")
    fpaths = glob.glob('Raspored_scraping/data/timetables/*.csv')
    if(len(fpaths) > 1):
        print('Found', len(fpaths), '.csv files.')
    elif(len(fpaths) == 0):
        print('Error: No .csv files found!')
        return

    Errors=[]
    
    for fpath in fpaths:
        #open csv file
        try:
            schedule:dict[str, set] = {}
            user = fpath.split("\\",1)[1].split("_",1)[0]
            if(user in cours_participants):
                print("Found student: ", cours_participants[user])
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
                    if not day in schedule:
                        schedule[day] = set()
                    schedule[day].add(time)
                cours_participants[user].schedule = schedule
                print(cours_participants[user].schedule["ponedjeljak"])
                    
        except Exception as e:
            print('Error with csv file', e)
            Errors.append(user)
            
    print("Errors with users: ", Errors, "\n")
    #24-02-2025
    #06-06-2025
