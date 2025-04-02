from labgenpackage.participants_parser import Student
from labgenpackage.schedule_parser import Group
import random


def fill_groups(cours_participants: dict[str, Student], groups: dict[str, list:Group]):
    lowestweightusers: list[str] = []
    biggestgroups: list[Group] = []
    lowest: int = 999999
    highest: int = 0
    username: str
    group: Group
    print(lowestweightusers)
    #Get users with lowest weights
    for username in cours_participants:
        if cours_participants[username].weight < lowest:
            lowest = cours_participants[username].weight
            lowestweightusers = []
            lowestweightusers.append(username)
        elif cours_participants[username].weight == lowest:
            lowestweightusers.append(username)

    print(len(lowestweightusers))
    print(lowestweightusers)
    
    #Get one random user with from lowestweightusers
    username = random.choice(lowestweightusers)
    #Get the biggest groups the selected user can join
    print(username, "weight:", cours_participants[username].weight)
    print("Groups:")
    print(*cours_participants[username].groups, sep="\n")
    for group in cours_participants[username].groups:
        if group.group_size > highest:
            highest = group.group_size
            biggestgroups = []
            biggestgroups.append(group)
        elif group.group_size == highest:
            biggestgroups.append(group)
    
    print("Biggest groups are")
    print(*biggestgroups, sep="\n")
    
    #Add user to one of the biggest groups at random
    group = random.choice(biggestgroups)
    print("Adding", username,"to group:",group)
    group.students.append(cours_participants[username])
    group.group_size -= 1
    cours_participants.pop(username)
    
    #Set new weights for all students
    for user in cours_participants.values():
        pass

    for day in groups:
        for group in groups[day]:
            print("In group:", group)
            print(*group.students, sep=", ")
