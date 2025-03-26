from participants_parser import pars_cours_participants
from schedule_parser import pars_schedule_file
from schedule_scraper import schedule_scraper
from weight_generator import weight_generator

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

#Get schedule for every student
try:
    schedule_scraper(cours_participants)
except Exception as e:
    print("Error when scraping schedule!")
    print("Exception: ", e)
    exit()

weight_generator()