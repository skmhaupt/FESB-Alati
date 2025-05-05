from labgenpackage.classes import Group
import logging
import glob

def pars_schedule_file()->tuple[Group,str]:

    logger = logging.getLogger("my_app.schedule_parsere")

    groups: dict[str, list:Group] = {}
    try:
        fpath: str
        fpaths: list = glob.glob("data/*.txt")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} .txt files, there can only be one!")
            raise FileNotFoundError
        elif(len(fpaths) == 0):
            logger.error("No .txt file found!")
            raise FileNotFoundError
        fpath = fpaths[0]

        with open(fpath,"r", encoding="utf8") as file:
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
        return (groups,fpath)

    except FileNotFoundError:
        raise logger.exception("The file 'data/schedule.txt' was not found.")
    except IOError:
        raise logger.exception("Error opening schedule file!")
    except Exception:
        raise logger.critical("Unexpected error in schedule parser!", exc_info=True)