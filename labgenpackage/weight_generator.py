from datetime import datetime
from labgenpackage.classes import Student
from labgenpackage.classes import Group
import logging

def weight_generator(cours_participants: dict[str, Student], groups: dict[str, list:Group]):
    
    logger = logging.getLogger("my_app.weight_generator")
    logger.setLevel("INFO")

    logger.info("Seting starting weights!")

    #For 'groups' structure check 'schedule_parser.py'
    #For 'cours_participants' structure check 'participants_parser.py'
    try:
        group: Group
        student: Student
        weight_errors: list[Student] = []

        for day in groups:
            logger.debug(f"Working on day: {day}")
            for group in groups[day]:
                logger.debug(f"Workong on group: {group}")
                for student in cours_participants.values():
                    canjoin: bool = True
                    dayappointments: list[list[datetime]] = student.schedule[day]
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
                        student.weight += group.group_size
                        student.groups.append(group)                    

        for user in cours_participants:
            if cours_participants[user].weight == 0:
                weight_errors.append(cours_participants[user])
                cours_participants.pop(user)
        
        if weight_errors:
            logger.critical(f"Found students that cant join any group! They will be skiped when filling out groups! The students are: {weight_errors}")
    
    except Exception:
        raise logger.error('Erro when seting starting weights!')