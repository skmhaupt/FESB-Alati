from labgenpackage.classes import Group
import logging
import glob
import re
from pathlib import Path
from os import path

def pars_schedule_file()->tuple[dict[str, list[Group]],str]:

    logger = logging.getLogger("my_app.schedule_parsere")
    logger.setLevel("INFO")

    groups: dict[str, list:Group] = {}
    try:
        delpath: Path
        fpath: str
        fpaths: list = glob.glob("data/*.txt")
        if(len(fpaths) > 1):
            logger.critical(f"Found {len(fpaths)} schedule \'.txt\' files, there can only be one!")
            logger.critical(f"Erasing all \'.txt\' files!")
            for pathstr in fpaths:
                logger.critical(f"Erasing {pathstr}")
                delpath = Path(pathstr)
                delpath.unlink()
            raise FileNotFoundError
        elif(len(fpaths) == 0):
            raise FileNotFoundError
        fpath = fpaths[0]
        file_name = path.basename(fpath)

        days = ["PON", "UTO", "SRI", "ČET", "PET"]
        with open(fpath,"r", encoding="utf8") as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace(' ', '')
                split_line = line.split(",")
                #Every line contains: group_label, day, time, lab, group_size
                if(len(split_line)==5):
                    if split_line[1] in days and re.fullmatch("[0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9]", split_line[2]) and re.fullmatch("[a-cA-C][1-9][0-9][0-9]", split_line[3]) and re.fullmatch("1?[0-9][0-9]?", split_line[4]):
                        group = Group(split_line[0], split_line[1], split_line[2], split_line[3], split_line[4])
                        if not group.day in groups:
                                groups[group.day] = []
                        groups[group.day].append(group)
        if(len(groups)==0):
            logger.error(f"Failed to finde groups in {fpath}")
            raise ValueError
        return (groups,file_name)

    except FileNotFoundError:
        logger.warning("The file 'data/schedule.txt' was not found.")
        raise
    except IOError:
        logger.critical("Error opening schedule file!")
        raise
    except Exception:
        logger.critical("Unexpected error in schedule parser!")
        raise