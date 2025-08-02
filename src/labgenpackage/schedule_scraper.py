import os, subprocess, logging
from subprocess import PIPE, STDOUT
from pathlib import Path
from labgenpackage.classes import Student

def log_subprocess_output(pipe, logger: logging):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logger.info('got line from subprocess: %r', line)

def schedule_scraper(cours_participants: dict[str, Student], dest_dir:str, startdate:str="", enddate:str=""):

    logger = logging.getLogger("my_app.schedule_scraper")
    logger.setLevel("INFO")

    try:
        os.chdir('Raspored_scraping')
        logger.info(f"Now in {os.getcwd()} directory!")
    except Exception:
        logger.critical("Failed to enter /Raspored_scraping directory.")
        raise

    logger.info("Creating/opening dates.txt file for Raspored_scraping.")
    try:
        dates_file = open("data/dates.txt", "w")

        dates_file.write(f"{startdate}\n")
        dates_file.write(f"{enddate}\n")
        dates_file.close()
    except Exception:
        logger.critical("Failed with dates.txt.")
        raise
    
    logger.info("Creating usernames.txt file for Raspored_scraping.")
    try:
        usernames_file = open("data/usernames.txt", "w")
        student: Student
        if cours_participants:
            for student in cours_participants.values():
                usernames_file.write(f"{student.username}\n")
            usernames_file.close()
    except Exception:
        logger.critical("Failed with usernames.txt.")
        raise

    if not cours_participants:
        logger.error("Coursparticipants not loaded.")
        try:
            os.chdir('..')
            logger.info(f"Now in {os.getcwd()} directory!\n")
        except Exception:
            logger.critical("Failed to exit /Raspored_scraping directory.")
            raise
        raise FileNotFoundError
    
    logger.info("Deleting old data from data/timetables!")
    try:
        folder =  Path("data/timetables")
        for item in folder.rglob("*"):
            item.unlink()
    except Exception:
        logger.critical(f"Failed to delete {item}")
        os.chdir('..')
        logger.info(f"Now in {os.getcwd()} directory!\n")
        raise

    logger.info("Launching schedule scraper!")
    try:
        #subprocess.run(['.\\gradlew', 'run'], shell=True, check=True)
        pro = subprocess.Popen('.\\gradlew run --no-daemon', shell=True, stdout=PIPE, stderr=STDOUT) #, preexec_fn=os.setsid
        with pro.stdout:
            log_subprocess_output(pro.stdout, logger)
        pro.wait()
    except subprocess.CalledProcessError:
        #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
        logger.critical("Error with running subprocess /gradlew")
        os.chdir('..')
        logger.info(f"Now in {os.getcwd()} directory!\n")
        raise

    os.chdir('..')
    logger.info(f"Now in {os.getcwd()} directory!\n")
    
    logger.info(f"Deleting old csv files in {dest_dir}")
    for filename in os.listdir(dest_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(dest_dir, filename)
            os.remove(file_path)
            logger.debug(f"Deleted file: {filename}")
    
    logger.info(f"Moving scraped csv files to {dest_dir}.")
    src_dir = "Raspored_scraping/data/timetables"
    for filename in os.listdir(src_dir):
        if filename.endswith(".csv"):
            src_file_path = os.path.join(src_dir, filename)
            dest_file_path = os.path.join(dest_dir, filename)
            os.rename(src_file_path, dest_file_path)
            #os.remove(src_file_path)
            logger.debug(f"Deleted file: {filename}")