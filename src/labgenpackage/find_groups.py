from labgenpackage.classes import Student
import datetime, logging

def FindeGroups(participatns: dict[str,Student], start_date:str, end_date:str, timeslot_length:int, using_breaks:bool) -> list[tuple[datetime,datetime]]:
    logger = logging.getLogger("my_app.finde_groups")
    logger.setLevel("INFO")

    appointments_all_can_join:list[tuple[datetime,datetime]] = []
    break_length = 15
    cours_length = 45
    num_of_breaks = timeslot_length - 1

    dd1,mm1,yyyy1 = start_date.split("-",2)
    dd2,mm2,yyyy2 = end_date.split("-",2)

    next_starttime_delta = datetime.timedelta(minutes=15)
    next_day_delta = datetime.timedelta(days=1)

    if using_breaks: timeslot_delta = datetime.timedelta(minutes=((timeslot_length * cours_length) + (num_of_breaks * break_length)))
    else: timeslot_delta = datetime.timedelta(minutes=(timeslot_length * cours_length))

    first_starttime_in_day = datetime.datetime(year=int(yyyy1), month=int(mm1), day=int(dd1), hour=8, minute=0)

    appointment_start = first_starttime_in_day
    appointment_end = appointment_start + timeslot_delta

    last_start_time = datetime.datetime(year=int(yyyy2), month=int(mm2), day=int(dd2), hour=20, minute=0)
    last_start_time_in_day = datetime.time(hour=20, minute=0)

    while appointment_start <= last_start_time:
        all_can_join = True
        date = appointment_start.date()
        date = f"{date}"
        ap_start_time = appointment_start.time()
        ap_end_time = appointment_end.time()
        can_join = []
        cant_join = []
        logger.debug("----------------------------------------------------------------")
        logger.debug(f"Date: {date}, Time slot: {ap_start_time} - {ap_end_time}")
        for student in participatns.values():
            if date in student.schedule.keys():
                student_ap_list = student.schedule[date]
                student_ap: tuple[datetime,datetime]

                for student_ap in student_ap_list:
                    student_ap_start = student_ap[0].time()
                    student_ap_end = student_ap[1].time()
                    if student_ap_start < ap_start_time and student_ap_end <= ap_start_time: 
                        can_join.append(student)
                        pass
                    elif student_ap_start >= ap_end_time: 
                        can_join.append(student)
                        pass
                    else: 
                        cant_join.append(student)
                        all_can_join = False
            
        if all_can_join:
            appointments_all_can_join.append((appointment_start, appointment_end))
        logger.debug(f"Students that can join: {can_join}")
        logger.debug(f"Students that can't join: {cant_join}")

        if appointment_start.time() == last_start_time_in_day:
            logger.debug("/////////////////////////////////////////////////////////////////")
            logger.debug("--- NEW DAY ---")
            first_starttime_in_day += next_day_delta
            appointment_start = first_starttime_in_day
        else:
            appointment_start += next_starttime_delta
        appointment_end = appointment_start + timeslot_delta

    logger.debug("/////////////////////////////////////////////////////////////////")
    logger.debug("Appointments all can join:")
    for appointment in appointments_all_can_join:
        date = appointment[0].date()
        ap_start_time = appointment[0].time()
        ap_end_time = appointment[1].time()
        logger.debug(f"Date: {date}, Time slot: {ap_start_time} - {ap_end_time}")
    
    return appointments_all_can_join