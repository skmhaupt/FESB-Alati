# global variables used in GUI
from customtkinter import BooleanVar

def init():
    # app data
    global cours_name, cours_number, acad_year, default_data_json

    # group gen data
    global start_date, end_date, loaded_data, working, total_places, cours_participants_global, alfa_prio_lvl, continue_answer, cours_participants_result
    global get_repeat_students, freed_if_passed_last  # BooleanVar

    # table gen data
    global ex_num, attendance, num_of_needed_passes, custom_ex_labels, max_test_points, min_average_required, student_coordinats
    global exempting_students, using_custom_exlabels, no_eval_ex0, using_lab0, not_using_failed_points  # BooleanVar

    # ---------------------------------------------------------------------
    # app data
    cours_name = ''
    cours_number = ''
    acad_year = ''
    default_data_json = {'cours':'', 'cours_number':'', 'acad_year':'', 'start_date':'', 'end_date':''}

    # ---------------------------------------------------------------------
    # group gen data
    start_date = ''
    end_date = ''

    # loaded_data is a collection of flags used to signal if main section 'fill_groups' can be launched
    # loaded_data = [groups_loaded, cours_loaded, participants_loaded, student_schedule_loaded]
    loaded_data = [False, False, False, False]

    # prevents multiple sections of running simultaneously to prevent unpredictable behaviour
    working = False

    # defines the total amount of places that are available with the provided groups in the .txt file
    total_places = 0

    # used for initial data loading for validation, and repeat students, it is not used in the main section 'fill_groups'
    cours_participants_global = None

    # flag that is used to store the users response when asked if he wants to proceed with the main section 'fill_groups'
    continue_answer = False

    # defines how strict the alfabetical weight has to be in comparison to space weight
    # W = ((space_weight / total_places) * (100 - alfa_prio_lvl)) + ((alf_position / total_num_of_students) * (alfa_prio_lvl))
    alfa_prio_lvl = 0

    cours_participants_result = None    # this will hold the final result
        
    num_of_needed_passes = 2    # defines number of passess needed for unconditional exemption

    exempting_students = BooleanVar(value=False)
    freed_if_passed_last = BooleanVar(value=True)

    # ---------------------------------------------------------------------
    # table gen data
    ex_num = 0
    attendance = 0

    custom_ex_labels = None

    using_custom_exlabels = BooleanVar(value=False)
    no_eval_ex0 = BooleanVar(value=False)
    using_lab0 = BooleanVar(value=False)
    not_using_failed_points = BooleanVar(value=True)
    get_repeat_students = BooleanVar(value=False)

    max_test_points = 0

    min_average_required = 0

    student_coordinats = {}