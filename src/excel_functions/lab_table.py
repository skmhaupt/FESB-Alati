from labgenpackage.classes import Student, Group

import openpyxl
import openpyxl.worksheet
import openpyxl.worksheet.worksheet

import xlsxwriter

import locale, re

# custom Exception class
class BadWorkbook(Exception):
    pass

# ------------------------------------------------
# excel functions

#Checks if loaded workbook is usable.
#Returns -> tuple[bool,bool] = (usable,type)
#usable: true = good workbook, false = bad workbook
#type: true = workbook from 'program', false = workbook from 'merlin'
def CheckForValidWorkbook(wb: openpyxl.Workbook, sh: openpyxl.worksheet.worksheet.Worksheet) -> tuple[bool,bool]:
    try:
        if not len(wb.sheetnames) == 1 or \
           not sh.max_column == 6 or \
           not sh.cell(row = 1, column = 1).value == "Prezime" or \
           not sh.cell(row = 1, column = 2).value == "Ime" or \
           not sh.cell(row = 1, column = 4).value == "ID broj":
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
        prezime = sh.cell(row = student_number+2, column = 1).value
        ime = sh.cell(row = student_number+2, column = 2).value
        email = sh.cell(row = student_number+2, column = 3).value
        jmbag = sh.cell(row = student_number+2, column = 4).value
        
        podatci_grupe = sh.cell(row = student_number+2, column = 6).value

        if podatci_grupe == "Još nisu odabrali":
            group = None
        else:
            # pars string containing group data
            grouplabel, rest = podatci_grupe.split(" - ",1)
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
        student = Student(ime,prezime,email,jmbag)
        if group:   # add group to student if he is in one
            student.group = group
        cours_participants.append(student)
    
    # sort created groups list and students list
    groups.sort(key=lambda x: natural_keys(x.group_label))
    locale.setlocale(locale.LC_COLLATE, "croatian")
    cours_participants.sort(key=lambda x: locale.strxfrm(x.surname))

    return cours_participants, groups


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
    width6 = len("Grupa")+2
    width7 = len("Priznat lab")+1
    width8 = len("Priznat jednom")+1
    width9 = len("Priznat dvaput")+1

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
        
        row+=1
    
    worksheet.set_column(0, 0, width1, format_left)
    worksheet.set_column(1, 1, width2, format_left)
    worksheet.set_column(2, 2, width3, format_left)
    worksheet.set_column(3, 3, width4, format_left)
    worksheet.set_column(4, 4, width5, format_left)
    worksheet.set_column(5, 5, width6, format_center)
    worksheet.set_column(6, 6, width7, format_left)
    worksheet.set_column(7, 7, width8, format_left)
    worksheet.set_column(8, 8, width9, format_left)

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

    worksheet.set_row(0, 30)



# ------------------------------------------------
# util functions
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


# ------------------------------------------------
# main function: for testing
if __name__=="__main__":
    cours_participants: list[Student] = []
    
    path = "2425-203450-9270_Odabir_grupa_za_lab._vježbe_202425.xlsx"
    new_file = "data\cours_workbook.xlsx"

    input_wb = openpyxl.load_workbook(filename=path)
    input_sh = input_wb.active

    usable, type = CheckForValidWorkbook(input_wb,input_sh)
    
    if not usable:
        quit()

    cours_participants, groups = LoadInputData(type, input_sh)
    
    out_wb = xlsxwriter.Workbook(new_file)
    WriteDataSheet(out_wb, cours_participants,groups)
    out_wb.close()
    