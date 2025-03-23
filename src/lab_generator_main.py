import subprocess
from participants_parser import pars_cours_participants
from schedule_parser import pars_schedule_file

#Get cours participants
try:
    cours_participants = pars_cours_participants()
    print('Found', len(cours_participants), 'students in participants file.')
except TypeError:
    print('Exiting script!')
    exit()

#Get lab group schedule
pars_schedule_file()

try:
    groups = pars_schedule_file()
    print('Found', len(groups), 'groups in schedule file.')
except TypeError:
    print('Exiting script!')
    exit()

print('Creating usernames.txt file for Raspored_scraping.')

#subprocess.run([".\gradlew", "run"], shell=True)