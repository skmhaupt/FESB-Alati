import os
import subprocess
from participants_parser import pars_cours_participants
from schedule_parser import pars_schedule_file

#Get cours participants
try:
    cours_participants = pars_cours_participants()
    print('Found', len(cours_participants), 'students in participants file.')
except TypeError:
    print('Exiting script from participants parsing!')
    exit()

#Get lab group schedule
try:
    groups = pars_schedule_file()
    print('Found', len(groups), 'groups in schedule file.')
except TypeError:
    print('Exiting script from schedule parsing!')
    exit()

print('Creating usernames.txt file for Raspored_scraping.')

os.chdir('Raspored_scraping')
print('Now in', os.getcwd(), 'directory!')
subprocess.run(['.\gradlew', 'run'], shell=True)
os.chdir('..')
print('Now in', os.getcwd(), 'directory!')