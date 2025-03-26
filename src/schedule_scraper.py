import os
import subprocess
import datetime

def schedule_scraper(students):
    date = datetime.datetime.now()
    #summer_semester_start_date = datetime.datetime(date.year, 2, 24)
    #winter_semester_start_date = datetime.datetime(date.year, 10, 1)
    os.chdir('Raspored_scraping')
    print('Now in', os.getcwd(), 'directory!')
    
    print('Creating dates.txt file for Raspored_scraping.')
    dates_file = open("data/dates.txt", "w")
    if date.month<10 and date.month>=2:
        print("In summer semester!")
        dates_file.write(f"1-3-{date.year}\n")
        dates_file.write(f"24-4-{date.year}\n")
    else:
        print("In winter semester!")
        dates_file.write(f"1-10-{date.year}\n")
        dates_file.write(f"15-12-{date.year}\n")
        dates_file.close()

    print('Creating usernames.txt file for Raspored_scraping.')
    usernames_file = open("data/usernames.txt", "w")
    for student in students:
        usernames_file.write(f"{student.username}\n")
    usernames_file.close()

    print("Launching schedule scraper!")
    #subprocess.run(['.\gradlew', 'run'], shell=True)

    os.chdir('..')
    print('Now in', os.getcwd(), 'directory!')


    #24-02-2025
    #06-06-2025