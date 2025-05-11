from labgenpackage.classes import Student
from labgenpackage.classes import Group
import random
import logging

def fill_groups(cours_participants: dict[str, Student], groups: dict[str, list[Group]], mode: int) -> tuple[bool,list[Student]]:

    logger = logging.getLogger("my_app.fill_groups")
    logger.setLevel("INFO")

    logger.info("Starting with filling out groups.")

    ret_value: tuple[bool,list[Student]]

    if mode == 0:
        ret_value = size_sort(cours_participants,groups,logger)
    elif mode == 1:
        ret_value = variable_sort(cours_participants,groups,logger)
    elif mode == 2:
        ret_value = alf_sort(cours_participants,groups,logger)
    else:
        logger.critical("Error with mode selection!")
        raise
    return ret_value

#----------------------------------------------------------------
def size_sort(cours_participants: dict[str, Student], groups: dict[str, list[Group]], logger: logging.Logger) -> bool:
    zero_weight_users: list[Student] = []
    
    while cours_participants:
        lowestweightusers: list[str] = []
        biggestgroups: list[Group] = []
        lowest: int = 999999
        highest: int = 1
        username: str
        group: Group
        #Get users with lowest weights
        for username in cours_participants:
            if cours_participants[username].weight < lowest:
                lowest = cours_participants[username].weight
                lowestweightusers = []
                lowestweightusers.append(username)
            elif cours_participants[username].weight == lowest:
                lowestweightusers.append(username)

        logger.debug(f"{len(lowestweightusers)} students with lowest weight: {*lowestweightusers,}")
        if lowest == 0:
            logger.critical(f"Lowest weight is '0'. Students {*lowestweightusers,} can not be added to any group!")
            for user in lowestweightusers:
                zero_weight_users.append(cours_participants[user])
                logger.warning(f"Removing {user} from cours_participants.")
                cours_participants.pop(user)
            continue
        
        #Get one random user with from lowestweightusers
        username = random.choice(lowestweightusers)
        logger.debug(f"User: {username} weight: {cours_participants[username].weight} chosen at random.")
        logger.debug(f"Student can join groups: {*cours_participants[username].groups,}")

        #Get the biggest groups the selected user can join
        for group in cours_participants[username].groups:
            if group.group_size > highest:
                highest = group.group_size
                biggestgroups = []
                biggestgroups.append(group)
            elif group.group_size == highest:
                biggestgroups.append(group)
        
        logger.debug(f"Biggest groups are: {*biggestgroups,}")
        
        #Add user to one of the biggest groups at random
        group = random.choice(biggestgroups)
        logger.debug(f"Adding {username} to group: {group}. (group is selected at random)")
        group.students.append(cours_participants[username])
        cours_participants[username].set_group(group)
        group.group_size -= 1
        cours_participants.pop(username)
        
        #Set new weights for all students
        logger.debug("Seting new weights for all users.")
        logger.debug("------------------------------------------------------------------")
        for user in cours_participants.values():
            user.update_weight()

    for day in groups:
        for group in groups[day]:
            logger.debug(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
            logger.debug("------------------------------------------------------------------")
    
    if zero_weight_users:
        logger.critical(f"No free group left for students: {*zero_weight_users,}")
        return False
    else: 
        return True

#----------------------------------------------------------------
def variable_sort(cours_participants: dict[str, Student], groups: dict[str, list[Group]], logger: logging.Logger) -> tuple[bool,list]:
    zero_weight_users: list[Student] = []

    while cours_participants:
        lowestweightusers: list[str] = []
        biggestgroups: list[Group] = []
        lowest: int = 999999
        highest: int = 1
        username: str
        group: Group

        #Get users with lowest weights
        for username in cours_participants:
            if cours_participants[username].variable_weight < lowest:
                lowest = cours_participants[username].variable_weight
                lowestweightusers = []
                lowestweightusers.append(username)
            elif cours_participants[username].variable_weight == lowest:
                lowestweightusers.append(username)

        logger.debug(f"{len(lowestweightusers)} students with lowest weight: {*lowestweightusers,}")
        logger.debug(f"lowest={lowest}")
        if lowest == 0:
            logger.critical(f"Lowest weight is '0'. Students {*lowestweightusers,} can not be added to any group!")
            for user in lowestweightusers:
                zero_weight_users.append(cours_participants[user])
                logger.warning(f"Removing {user} from cours_participants.")
                cours_participants.pop(user)
            continue

        #Get one random user with from lowestweightusers
        username = random.choice(lowestweightusers)
        logger.debug(f"User: {username} variable_weight: {cours_participants[username].variable_weight} chosen at random.")
        logger.debug(f"Student can join groups: {*cours_participants[username].groups,}")

        #Get the first group that hase room the selected user can join
        found_group: bool = False
        for group in cours_participants[username].groups:
            logger.debug(f"Testing group {group} with size {group.group_size}")
            if group.group_size > 0:
                found_group = True
                break
        #Check if even last group has size 0
        if not found_group:
            logger.critical(f"Selected lowest weight user {cours_participants[username]} can not be added to any group!")
            zero_weight_users.append(cours_participants[username])
            logger.warning(f"Removing {cours_participants[username]} from cours_participants.")
            cours_participants.pop(username)
            continue
        
        logger.debug(f"Selected group is: {group}.")

        #Add user to selected group
        logger.debug(f"Adding {username} to group: {group}.")
        group.students.append(cours_participants[username])
        cours_participants[username].set_group(group)
        group.group_size -= 1
        cours_participants.pop(username)
        
        #Set new weights for all students
        logger.debug("Seting new weights for all users.")
        logger.debug("------------------------------------------------------------------")
        for user in cours_participants.values():
            user.update_weight()
            user.update_var_weight()

    for day in groups:
        for group in groups[day]:
            logger.info(f"Group: {group} filled with {len(group.students)} students: {*group.students,}")
            logger.info("------------------------------------------------------------------")
    
    if zero_weight_users:
        logger.critical(f"No free group left for students: {*zero_weight_users,}")
        return (False,zero_weight_users)
    else: return (True,[])

#----------------------------------------------------------------
def alf_sort(cours_participants: dict[str, Student], groups: dict[str, list:Group], logger: logging.Logger):
    pass