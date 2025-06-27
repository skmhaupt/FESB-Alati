# global variables used in GUI
def init():
    global loaded_data, total_places, cours_participants_global, alfa_prio_lvl, total_places, continue_answer, working, cours_participants_result, cours_name, cours_number
    
    # loaded_data is a collection of flags used to signal if main section 'fill_groups' can be launched
    # loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
    loaded_data = [False, False, False, False]

    # prevents multiple sections of running simultaneously to prevent unpredictable behaviour
    working = False

    # this variable defines the total amount of places that are available with the provided groups in the .txt file
    total_places = 0

    # this variable is only used for initial data loading for validation, it is not used in the main section 'fill_groups'
    cours_participants_global = None

    # flag that is used to store the users response when asked if he wants to proceed with the main section 'fill_groups'
    continue_answer = False

    # 
    alfa_prio_lvl = 0

    # this will hold the final resultgit 
    cours_participants_result = None

    cours_name = ""
    cours_number = ""