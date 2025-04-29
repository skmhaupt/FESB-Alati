from datetime import datetime
from labgenpackage.classes import Student
from labgenpackage.classes import Group
import logging

def weight_generator(cours_participants: dict[str, Student], groups: dict[str, list:Group],alf_prio_lvl: int):
    
    logger = logging.getLogger("my_app.weight_generator")
    logger.setLevel("INFO")

    logger.info("Setting starting weights!")

    #For 'groups' structure check 'schedule_parser.py'
    #For 'cours_participants' structure check 'participants_parser.py'

    #Setting up group weights
    try:
        group: Group
        student: Student
        weight_errors: list[Student] = []
        total_places: int = 0

        for day in groups:
            logger.debug(f"Working on day: {day}")
            for group in groups[day]:
                logger.debug(f"Workong on group: {group}")
                total_places += group.group_size
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

        for user in cours_participants.copy():
            if cours_participants[user].weight == 0:
                weight_errors.append(cours_participants[user])
                cours_participants.pop(user)
        
        if weight_errors:
            logger.critical(f"Found students that cant join any group! They will be skiped when filling out groups! The number of students is: {len(weight_errors)}. The students are: {weight_errors}")
    
    except Exception:
        logger.error("Erro when seting group weights!")
        raise
    
    #Setting up alfabetical weights
    try:
        counter: int = 1
        for student in cours_participants.values():
            student.position = counter
            student.set_alf_weight(len(cours_participants))
            student.set_group_weight(total_places)
            student.set_var_weight(alf_prio_lvl)
            counter += 1
            #logger.info(f"{*cours_participants,}")
    except Exception:
        logger.error('Erro when seting alfabetical weights!')
        raise