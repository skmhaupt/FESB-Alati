from labgenpackage.classes import Student, Group
from gui.util import CopyAndRename
from pathlib import Path

import openpyxl.worksheet.worksheet
import openpyxl.worksheet
import openpyxl
import gui.settings as settings
import xlsxwriter, locale, re

# custom Exception class
class BadWorkbook(Exception):
    pass

# -------------------------------------------------------------------------------
# excel functions

# Checks if loaded workbook is usable.
# Returns -> tuple[bool,bool] = (usable,type)
# usable: true = good workbook, false = bad workbook
# type: true = workbook from 'program', false = workbook from 'merlin'
def CheckForValidWorkbook(wb: openpyxl.Workbook, sh: openpyxl.worksheet.worksheet.Worksheet) -> tuple[bool,bool]:
    try:
        if not len(wb.sheetnames) == 1 or \
           not sh.max_column == 6 or \
           not sh.cell(row = 1, column = 1).value == "Prezime" or \
           not sh.cell(row = 1, column = 2).value == "Ime" or \
           not (sh.cell(row = 1, column = 4).value == "ID broj" or "JMBAG"):
            raise BadWorkbook("Loaded workbook is not apropriet.")
        
        if sh.cell(row = 1, column = 3).value == "Email" and \
           sh.cell(row = 1, column = 5).value == "Korisničko ime" and \
           sh.cell(row = 1, column = 6).value == "Grupa":
            print("Loaded workbook from 'program'.")
            return True,True
        elif sh.cell(row = 1, column = 3).value == "Korisničko ime" and \
             sh.cell(row = 1, column = 5).value == "Grupa" and \
             sh.cell(row = 1, column = 6).value == "Odabir {$a}":
            print("Loaded workbook from 'merlin'.")
            return True,False
        else:
            raise BadWorkbook("Loaded workbook is not apropriet.")
        
    except BadWorkbook as e:
        print(e)
        return False,False
    except Exception:
        print("Unexcpected error when validating workbook!")
        raise

# -----------------------------------------------------------
# Loads all data from workbook
# Returns -> tuple[list[Student], list[Group]] = (cours_participants,groups)
# cours_participants: alfabeticly sorted students
# groups: naturaly sorted groups
def LoadInputData(type: bool, sh: openpyxl.worksheet.worksheet.Worksheet) -> tuple[list[Student], list[Group]]:
    num_of_students = sh.max_row - 1
    cours_participants: list[Student] = []
    groups: list[Group] = []
    grouplabels: set[str] = set()
    group: Group = None

    # get all student and group data
    for student_number in range(num_of_students):
        surname = sh.cell(row = student_number+2, column = 1).value
        name = sh.cell(row = student_number+2, column = 2).value
        email = sh.cell(row = student_number+2, column = 3).value
        jmbag = sh.cell(row = student_number+2, column = 4).value
        
        group_data = sh.cell(row = student_number+2, column = 6).value

        if group_data == "Još nisu odabrali":
            group = None
        else:
            # pars string containing group data
            grouplabel, rest = group_data.split(" - ",1)
            day, rest = rest.split(" ", 1)
            time, rest = rest.split(" (")
            room = rest.removesuffix(")")
            time = time.replace(" ", "")

            # create group or update if existing
            if grouplabel in grouplabels:   # update existing group
                group = next((group for group in groups if group.group_label == grouplabel), None)
                group.group_size += 1
            else:   # create new group
                grouplabels.add(grouplabel)
                group = Group(grouplabel,day,time,room,1)
                groups.append(group)

        # create new student
        student = Student(name,surname,email,jmbag)
        if group:   # add group to student if he is in one
            student.group = group
            group.students.append(student)
        cours_participants.append(student)
    
    # sort created groups list and students list
    groups.sort(key=lambda x: natural_keys(x.group_label))
    locale.setlocale(locale.LC_COLLATE, "croatian")
    cours_participants.sort(key=lambda x: locale.strxfrm(x.surname))

    return cours_participants, groups

# -----------------------------------------------------------
# Writes sheet with all student data (name, JMABG, username, Email, Group, ...)
def WriteDataSheet(workbook: xlsxwriter.Workbook, cours_participants: list[Student], groups: list[Group]):
    worksheet = workbook.add_worksheet()

    format_left = workbook.add_format({'align': 'left'})
    format_center = workbook.add_format({'align': 'center'})
    format_header = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'center', 'bg_color': '#BFBFBF'})

    worksheet.name = "Studenti"
    worksheet.write("A1", "Prezime",format_header)
    worksheet.write("B1", "Ime",format_header)
    worksheet.write("C1", "JMBAG",format_header)
    worksheet.write("D1", "Korisničko ime",format_header)
    worksheet.write("E1", "Email",format_header)
    worksheet.write("F1", "Grupa",format_header)
    worksheet.write("G1", "Priznat lab",format_header)
    worksheet.write("H1", "Priznat jednom",format_header)
    worksheet.write("I1", "Priznat dvaput",format_header)

    width1 = len("Prezime")+1
    width2 = len("Ime")+1
    width3 = len("JMBAG")+1
    width4 = len("Korisničko ime")+1
    width5 = len("Email")+1
    width6 = 11 # grupa
    width7 = 15 # Priznat lab
    width8 = 19 # Priznat jednom
    width9 = 19 # Priznat dvaput

    row: int = 2
    for student in cours_participants:
        worksheet.write(f"A{row}", student.surname)
        worksheet.write(f"B{row}", student.name)
        worksheet.write(f"C{row}", student.jmbag)
        worksheet.write(f"D{row}", student.username)
        worksheet.write(f"E{row}", student.email)
        if hasattr(student, 'group'):
            worksheet.write(f"F{row}", f"{student.group.group_label}")
        else:
            worksheet.write(f"F{row}", "G0")
        
        if len(student.surname) > width1: width1 = len(student.surname)+1
        if len(student.name) > width2: width2 = len(student.name)+1
        if len(str(student.jmbag)) > width3: width3 = len(str(student.jmbag))+4
        if len(student.username) > width4: width4 = len(student.username)+1
        if len(student.email) > width5: width5 = len(student.email)+4
        if hasattr(student, 'group'):
            if len(f"{student.group.group_label}") > width6: width6 = len(f"{student.group.group_label}")+1
        
        worksheet.set_row(row-1, 18)  # student rows -> height 30px

        row+=1
    
    worksheet.set_column(0, 0, width1, format_left)
    worksheet.set_column(1, 1, width2, format_left)
    worksheet.set_column(2, 2, width3, format_center)
    worksheet.set_column(3, 3, width4, format_center)
    worksheet.set_column(4, 4, width5, format_center)
    worksheet.set_column(5, 5, width6, format_center)
    worksheet.set_column(6, 6, width7, format_center)
    worksheet.set_column(7, 7, width8, format_center)
    worksheet.set_column(8, 8, width9, format_center)

    worksheet.write("L1", "Grupa",format_header)
    worksheet.write("M1", "Dan",format_header)
    worksheet.write("N1", "Vrijeme",format_header)
    worksheet.write("O1", "Dvorana",format_header)

    width1 = len("Grupa")+2
    width2 = len("Dan")+3
    width3 = len("Vrijeme")+2
    width4 = len("Dvorana")+2
    
    row = 2
    for group in groups:
        worksheet.write(f"L{row}", group.group_label)
        worksheet.write(f"M{row}", group.day)
        worksheet.write(f"N{row}", group.time)
        worksheet.write(f"O{row}", group.lab)

        if len(group.group_label) > width1:width1 = len(group.group_label)+1
        if len(group.day) > width2: width2 = len(group.day)+1
        if len(group.time) > width3: width3 = len(group.time)+1
        if len(group.lab) > width4: width4 = len(group.lab)+1
        
        row+=1
        
    worksheet.set_column(11, 11, width1, format_center)
    worksheet.set_column(12, 12, width2, format_center)
    worksheet.set_column(13, 13, width3, format_center)
    worksheet.set_column(14, 14, width4, format_center)

    worksheet.set_row(0, 30)    # set row 1 height

    worksheet.autofilter(0,5, len(cours_participants),8)    # filter by groups and exemptions

# -----------------------------------------------------------
# Writes sheet that containes all points, average and attendance
def WritePointsSheet(workbook: xlsxwriter.Workbook, cours_participants: list[Student], groups: list[Group]):
    worksheet = workbook.add_worksheet()

    format_header = workbook.add_format({'font_size': 12, 'bold': False, 'text_wrap': True, 'align': 'center', 'bg_color': '#BFBFBF', 'left':0, 'right':0, 'border':1, 'bottom':5 , 'top':5})
    format_name_header = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'center', 'bg_color': '#BFBFBF', 'border':1, 'left':5, 'right':5, 'bottom':5 , 'top':5})
    format_average_header = workbook.add_format({'font_size': 12, 'bold': False, 'align': 'center', 'bg_color': '#BFBFBF', 'border':1, 'left':0, 'right':5, 'bottom':5 , 'top':5})
    
    format_students = workbook.add_format({'align': 'left', 'border':1, 'left':5, 'right':5, 'bottom':0 , 'top':0})
    format_last_student = workbook.add_format({'align': 'left', 'border':1, 'left':5, 'right':5, 'bottom':5 , 'top':0 })
    format_bottom = workbook.add_format({'border':1, 'left':0, 'right':0, 'bottom':0, 'top':5 })


    worksheet.name = "Bodovi"
    worksheet.write("A1", "Prezime i Ime",format_name_header)
    
    # --------------------------------------
    # write header
    row=0
    col=0
    for ex in range(settings.ex_num):
        col+=1
        worksheet.write(row, col, f"LAB{ex+1}",format_header)
    col+=2   # skip one column
    worksheet.write(row, col, f"ZADOVOLJENA PRISUTNOST",format_header)
    worksheet.set_column(col, col, 14)  # col 'ZADOVOLJENA PRISUTNOST' -> width 133px
    col+=1
    worksheet.write(row, col, f"PROSJEK",format_average_header)
    worksheet.set_column(col, col, 9)   # col 'PROSJEK' -> width 88px
    worksheet.set_row(0, 33)    # row 1 -> height 55px

    # -------------------
    # write students
    width1 = len("Prezime i Ime")+1
    row: int = 2
    for student in cours_participants:
        if row == len(cours_participants)+1: format = format_last_student
        else: format = format_students
        worksheet.write(f"A{row}", student.fullname, format)
        if len(student.fullname) > width1: width1 = len(student.fullname)+1
        worksheet.set_row(row-1, 18)  # student rows -> height 30px
        row+=1
    col=1
    for index in range(settings.ex_num+3):
        worksheet.write(row-1,  col+index, "", format_bottom)
    worksheet.set_column(0, 0, width1)
    
# -----------------------------------------------------------
# Writes sheet with all filled group tables
def WriteTablesSheet(workbook: xlsxwriter.Workbook, groups: list[Group]):
    worksheet = workbook.add_worksheet()

    format_header = workbook.add_format({'font_size': 15, 'bold': True, 'align': 'center'})
    
    format_fullname_label = workbook.add_format({'border':1, 'left':1, 'right':1, 'bottom':5 , 'top':5})
    format_ex_label = workbook.add_format({'align': 'center', 'bg_color': '#BFBFBF', 'border':1, 'left':1, 'right':1, 'bottom':5 , 'top':5})
    format_last_ex_label = workbook.add_format({'align': 'center', 'bg_color': '#BFBFBF', 'border':1, 'left':1, 'right':5, 'bottom':5 , 'top':5})
    format_group_label = workbook.add_format({'border':1, 'left':5, 'right':5, 'bottom':5 , 'top':5})
    
    format_empty_cell = workbook.add_format({'border':1, 'left':5, 'right':1, 'bottom':1 })
    
    format_first_index_label = workbook.add_format({'align': 'left', 'border':1, 'left':5, 'right':1, 'bottom':1 , 'top':5})
    format_index_label = workbook.add_format({'align': 'left', 'border':1, 'left':5, 'right':1, 'bottom':1 , 'top':1})
    format_last_index_label = workbook.add_format({'align': 'left', 'border':1, 'left':5, 'right':1, 'bottom':5 , 'top':1})

    format_center_cell = workbook.add_format({'border':1, 'right':1, 'bottom':1})
    format_right_moste_center_cell = workbook.add_format({'border':1, 'right':5, 'bottom':1})
    format_last_row_center_cell = workbook.add_format({'border':1, 'right':1, 'bottom':5})
    format_right_moste_last_row_center_cell = workbook.add_format({'border':1, 'right':5, 'bottom':5})

    worksheet.name = "Tablice"
    if settings.cours_name == "":
        worksheet.write("E1", "Predmet Smjer",format_header)
    else:
        worksheet.write("E1", f"{settings.cours_name} {settings.cours_number}",format_header)
    worksheet.write("E2", "LABORATORIJSKE VJEŽBE FESB",format_header)

    max_group_size: int = 0
    for group in groups:
        if max_group_size < group.group_size: max_group_size = group.group_size

    row: int = 5
    col: int = 0
    group_label_width = 4
    student_width = len("Prezime i Ime")
    for group in groups:
        starting_row = row
        if len(group.group_label) > group_label_width: group_label_width = len(group.group_label)
        worksheet.write(row, col, f"{group.group_label}", format_group_label)
        worksheet.write(row, col+1, f"{group.day} {group.time}", format_group_label)
        worksheet.write(row, col+2, f"{group.lab}", format_group_label)
        worksheet.set_row(row, 16)  # label rows -> height px
        row+=1  # move to next row
        worksheet.write(row, col, "", format_empty_cell)
        worksheet.write(row, col+1, "Prezime i Ime", format_fullname_label)
        for ex in range(settings.ex_num):   # write ex labels
            if ex == settings.ex_num-1: format = format_last_ex_label
            else: format = format_ex_label
            worksheet.write(row, col+2+ex, f"Lab{ex+1}", format)
        worksheet.set_row(row, 16)  # label rows -> height px

        row+=1  # move to next row
        index = 1
        for student in group.students:  # add students to table and format row
            if index == 1: format = format_first_index_label
            else: format = format_index_label
            format2 = format_center_cell
            worksheet.write(row, col, index, format)
            worksheet.write(row, col+1, f"{student.fullname}", format2)
            if student_width < len(student.fullname): student_width = len(student.fullname)
            for index2 in range(settings.ex_num):
                if index2 == settings.ex_num-1: format2 = format_right_moste_center_cell
                worksheet.write(row, col+2+index2, "", format2)
            worksheet.set_row(row, 18)  # student rows -> height 30px
            row+=1  # move to next row
            index+=1

        while index < max_group_size+2: # padd with empty group slots
            if index == 1: 
                format = format_first_index_label
                format2 = format_center_cell
            elif index == max_group_size+1: 
                format = format_last_index_label
                format2 = format_last_row_center_cell
            else: 
                format = format_index_label
                format2 = format_center_cell
            worksheet.write(row, col, index, format)
            worksheet.write(row, col+1, "",format2)
            for index2 in range(settings.ex_num):
                if index == max_group_size+1 and index2 == settings.ex_num-1: format2 = format_right_moste_last_row_center_cell
                elif index2 == settings.ex_num-1: format2 = format_right_moste_center_cell
                worksheet.write(row, col+2+index2, "", format2)
            worksheet.set_row(row, 18)  # student rows -> height 30px
            row+=1
            index+=1
        # move to next table location
        if col == 0: 
            row = starting_row
            col = col + 3 + settings.ex_num
        else:
            row = row + 4
            col = 0

    worksheet.set_column(0, 0, group_label_width)
    worksheet.set_column(3+settings.ex_num, 3+settings.ex_num, group_label_width)
    worksheet.set_column(1, 1, student_width)
    worksheet.set_column(4+settings.ex_num, 4+settings.ex_num, student_width)
    
# -----------------------------------------------------------
def LinkTableAndPointsSheet():
    pass
    
# -----------------------------------------------------------
# util functions
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


# -----------------------------------------------------------
# Main function for call
# Returns -> bool = (success)
def gen_tables(input_file: str)-> bool:
    new_file = "data/cours_workbook.xlsx"

    input_wb = openpyxl.load_workbook(filename=input_file)
    input_sh = input_wb.active

    usable, type = CheckForValidWorkbook(input_wb,input_sh)
    
    if not usable:
        return False

    cours_participants, groups = LoadInputData(type, input_sh)
    
    out_wb = xlsxwriter.Workbook(new_file)
    WriteDataSheet(out_wb, cours_participants, groups)
    WritePointsSheet(out_wb, cours_participants, groups)
    WriteTablesSheet(out_wb, groups)
    out_wb.close()

    CopyAndRename(srcname="cours_workbook.xlsx", dstname="lab_tablice")
    
    delpath=Path(new_file)
    delpath.unlink()
    return True