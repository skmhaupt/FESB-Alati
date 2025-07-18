# global variables used in GUI
from customtkinter import BooleanVar

def init():
    global loaded_data, total_places, cours_participants_global, alfa_prio_lvl, total_places, continue_answer, working, cours_participants_result, cours_name, cours_number, ex_num, attendance, custom_ex_labels, max_test_points, min_average_required
    global using_custom_exlabels, no_eval_ex0, using_lab0, not_using_failed_points, get_repeat_students  # BooleanVar
    global student_coordinats

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

    ex_num = 0
    attendance = 0

    custom_ex_labels = None

    using_custom_exlabels = BooleanVar(value=False)
    no_eval_ex0 = BooleanVar(value=False)
    using_lab0 = BooleanVar(value=False)
    not_using_failed_points = BooleanVar(value=False)
    get_repeat_students = BooleanVar(value=False)

    max_test_points = 0

    min_average_required = 0

    student_coordinats = {}