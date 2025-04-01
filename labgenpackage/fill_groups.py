from labgenpackage.participants_parser import Student
from labgenpackage.schedule_parser import Group
import random


def fill_groups(cours_participants: dict[str, Student], groups: dict[str, list:Group]):
    lowestweightusers: list[str] = []
    biggestgroups: list[Group] = []
    lowest: int = 300
    username: str
    print(lowestweightusers)
    for username in cours_participants:
        if cours_participants[username].weight < lowest:
            lowest = cours_participants[username].weight
            lowestweightusers = []
            lowestweightusers.append(username)
        elif cours_participants[username].weight == lowest:
            lowestweightusers.append(username)

    print(len(lowestweightusers))
    print(lowestweightusers)

    for username in lowestweightusers:
        print(username, "weight:", cours_participants[username].weight)
        print("Groups:")
        print(*cours_participants[username].groups, sep="\n")
        group = random.choice(cours_participants[username].groups)
        print("From cours participants",group)
        group.group_size -= 1
        print("From cours participants: ",group)
        print("From groups: ",groups["PON"][0])
    
    