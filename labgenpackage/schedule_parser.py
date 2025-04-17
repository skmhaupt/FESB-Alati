from labgenpackage.classes import Group
import logging

def pars_schedule_file():

    logger = logging.getLogger("my_app.schedule_parsere")

    groups: dict[str, list:Group] = {}
    try:
        with open('data/schedule.txt',"r", encoding="utf8") as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                split_line = line.split(",")
                #Every line contains: group_label, day, time, lab, group_size
                if(len(split_line)==5):
                    group = Group(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4])
                    if not group.day in groups:
                            groups[group.day] = []
                    groups[group.day].append(group)
        if(len(groups)==0):
            raise logger.error("Error: Failed to finde groups in \'data/schedule.txt!\'")    
        return groups

    except FileNotFoundError:
        raise logger.exception("The file 'data/schedule.txt' was not found.")
    except IOError:
        raise logger.exception("Error opening schedule file!")
    except Exception:
        raise logger.critical("Unexpected error in schedule parser!", exc_info=True)