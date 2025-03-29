from datetime import datetime
from labgenpackage.participants_parser import Student
from labgenpackage.schedule_parser import Group
import traceback
import logging

def weight_generator(cours_participants: dict[str, Student], groups: dict[str, list:Group]):
    print("Seting starting weights!")
    days = ["PON", "UTO", "SRI", "ČET", "PET"]
    
    #For 'groups' structure check 'schedule_parser.py'
    #For 'cours_participants' structure check 'participants_parser.py'
    try:

        for day in days:
            group: Group
            for group in groups[day]:
                for username in cours_participants:
                    canjoin: bool = True
                    dayappointments: list[list[datetime]] = cours_participants[username].schedule[day]
                    #check if dayappointments is empty
                    if dayappointments:
                        appointment: list[datetime]
                        for appointment in dayappointments:
                            appstarttime: datetime = appointment[0]
                            appendtime: datetime = appointment[1]
                            #check if group overlaps with schedule
                            if group.starttime <= appstarttime < group.endtime:
                                canjoin = False
                            elif group.starttime < appendtime <= group.endtime:
                                canjoin = False
                    
                    if canjoin:
                        cours_participants[username].weight += group.group_size
                        cours_participants[username].groups.append(group)
    except Exception as e:
        print('Erro when seting starting weights!')
        logging.error(traceback.format_exc)
        raise e