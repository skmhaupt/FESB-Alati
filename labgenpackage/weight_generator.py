from datetime import datetime
from labgenpackage.participants_parser import Student
from labgenpackage.schedule_parser import Group

def get_times():
    pass

def weight_generator(cours_participants: dict[str, Student], groups: dict[str, list:Group]):
    print("Seting starting weights!")
    days = ["PON", "UTO", "SRI", "ČET", "PET"]
    days2 = {
        "PON": "ponedjeljak",
        "UTO": "utorak",
        "SRI": "srijeda",
        "ČET": "četvrtak",
        "PET": "petak"
    }
    for day in days:
        #print(day)
        group: Group
        for group in groups[day]:
            #print("Grupa ", group.group_number,": ", group.starttime, "-", group.endtime)
            #print(group)
            for username in cours_participants:
                canjoin: bool = True
                dayappointments: list = cours_participants[username].schedule[day]
                #print(username, "schedule: ", dayappointments)
                if dayappointments:
                    for appointment in dayappointments:
                        #print("Appointment: ", appointment[0], "-", appointment[1])
                        appstarttime = appointment[0]
                        appendtime = appointment[1]
                        if group.starttime <= appstarttime < group.endtime:
                            canjoin = False
                            #print(group.time, "overlaps with", appstarttime,"-",appendtime)
                        elif group.starttime < appendtime <= group.endtime:
                            canjoin = False
                            #print(group.time, "overlaps with", appstarttime,"-",appendtime)
                        #else:
                            #pass
                            #print("ajelin00 can join group", group.group_number)
                    #if canjoin:
                        #print("ajelin00 can join group", group.group_number)
                        #cours_participants[username].weight += group.group_size
                        #cours_participants[username].groups.append(group)
                    #else:
                        #print("ajelin00 can't join group", group.group_number)
                if canjoin:
                    #print("Free")
                    #print("ajelin00 can join group", group.group_number)
                    cours_participants[username].weight += group.group_size
                    cours_participants[username].groups.append(group)
                #print("\n")
        #print("-----------------------\n")