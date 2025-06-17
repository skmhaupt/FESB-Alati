# global variables used in GUI

def init():
    global loaded_data, total_places, cours_participants_global, alfa_prio_lvl, total_places, continue_answer, working
    
    #loaded_data is a collection of flags used to signal if main section 'fill_groups' can be launched
    #loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
    loaded_data = [False, False, False, False]

    #this variable defines the total amount of places that are available with the provided groups in the .txt file
    total_places = 0

