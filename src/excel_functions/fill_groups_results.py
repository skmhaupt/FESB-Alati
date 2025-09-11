from labgenpackage.classes import Student

import gui.settings as settings
import xlsxwriter, logging, locale

def GenScraperDetailesWorkbook(csvMissing:list[Student], csvEmpty:list[Student]):
    try:
        workbook = xlsxwriter.Workbook("data/Student_schedules_Error_detailes.xlsx")
        worksheet = workbook.add_worksheet()

        merge_format = workbook.add_format({"border":1, "bottom":5, "align": "center"})
        center_format = workbook.add_format({'align': 'center'})
        jmbag_format = workbook.add_format({'num_format': '0000000000', 'align': 'center'})

        worksheet.write("A2", "Ime i prezime", center_format)
        worksheet.write("B2", "JMBAG", center_format)
        worksheet.write("C2", "E-Mail", center_format)

        worksheet.write("E2", "Ime i prezime", center_format)
        worksheet.write("F2", "JMBAG", center_format)
        worksheet.write("G2", "E-Mail", center_format)
        
        width1 = 17 # 160px
        width2 = 13 # 124px
        width3 = 17 # 160px
        row: int = 3
        for student in csvMissing:
            worksheet.write(f"A{row}", f"{student.fullname}")
            if width1 < len(f"{student.fullname}"):
                width1 = len(f"{student.fullname}")+1

            worksheet.write(f"B{row}", student.jmbag, jmbag_format)

            worksheet.write(f"C{row}", f"{student.email}")
            if width3 < len(f"{student.email}"):
                width3 = len(f"{student.email}")+1

            row += 1

        worksheet.set_column(0, 0, width1)
        worksheet.set_column(1, 1, width2)
        worksheet.set_column(2, 2, width3)
        worksheet.merge_range("A1:C1", "Studenti kojima nije uspjesno preuzet raspored", merge_format)
        
        width1 = len("Ime i prezime")+1
        width3 = len("E-Mail")+1
        row: int = 3
        for student in csvEmpty:
            #worksheet.write(f"C{row}", f"{student}")
            worksheet.write(f"E{row}", f"{student.fullname}")
            if width1 < len(f"{student.fullname}"):
                width1 = len(f"{student.fullname}")+1

            worksheet.write(f"F{row}", student.jmbag, jmbag_format)

            worksheet.write(f"G{row}", f"{student.email}")
            if width3 < len(f"{student.email}"):
                width3 = len(f"{student.email}")+1

            row += 1

        worksheet.set_column(4, 4, width1)
        worksheet.set_column(5, 5, width2)
        worksheet.set_column(6, 6, width3)
        worksheet.merge_range("E1:G1", "Studenti kojima je preuzet raspored prazan", merge_format)

        workbook.close()

    except Exception:
        raise


def GenErrorDetailsWorkbook(logger: logging.Logger, weight_errors:list[Student], fill_errors:list[Student]):
    try:
        workbook = xlsxwriter.Workbook("data/Error_detailes.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write("A1", f"Broj studenta kojima ne odgovara niti jedna grupa: {len(weight_errors)}", workbook.add_format({"border":2, "bottom":1}))
        worksheet.write("A2", f"Broj studenta koji nisu uspjesno svrstani u grupu: {len(fill_errors)}", workbook.add_format({"border":2, "top":1}))
        worksheet.write("A4", "Studenti")
        worksheet.write("B4", "Dostupne grupe")
        worksheet.write("C4", "Nesvrstani studenti")
        worksheet.write("D4", "Dostupne grupe")
        worksheet.write("E4", "Studenti bez grupe")

        width1 = len("Studenti")+1
        width2 = len("Dostupne grupe")+1
        width3 = len("Nesvrstani studenti")+1
        width4 = len("Dostupne grupe")+1
        width5 = len("Studenti bez grupe")+1

        f1=workbook.add_format({"border":1, "left":5, "right":5})   #Thick left and right
        f2=workbook.add_format({"border":1, "right":5})             #Thick right
        f3=workbook.add_format({"border":1, "left":5})              #Thick left

        row: int = 5
        student: Student
        for student in settings.cours_participants_result.values():
            worksheet.write(f"A{row}", f"{student}", f3)
            if hasattr(student, "groups"):
                worksheet.write(f"B{row}", f"{*student.groups,}", f2)
                if width2 < len(f"{*student.groups,}"):
                    width2 = len(f"{*student.groups,}")
            else:
                worksheet.write(f"B{row}", "Bez grupe")

            if width1 < len(f"{student}"):
                width1 = len(f"{student}")+1
            
            row += 1
        
        row: int = 5
        for student in fill_errors:
            worksheet.write(f"C{row}", f"{student}", f3)
            if hasattr(student, "groups"):
                worksheet.write(f"D{row}", f"{*student.groups,}", f2)
                if width4 < len(f"{*student.groups,}"):
                    width4 = len(f"{*student.groups,}")
            else:
                worksheet.write(f"D{row}", "Bez grupe")
            
            if width3 < len(f"{student}"):
                width3 = len(f"{student}")+1

            row += 1
        
        row: int = 5
        for student in weight_errors:
            worksheet.write(f"E{row}", f"{student}", f1)
            if width5 < len(f"{student}"):
                width5 = len(f"{student}")+1
            row += 1
        
        worksheet.set_column(0, 0, width1)
        worksheet.set_column(1, 1, width2)
        worksheet.set_column(2, 2, width3)
        worksheet.set_column(3, 3, width4)
        worksheet.set_column(4, 4, width5)

        workbook.close()
    except Exception:
        logger.critical("Error with creating Error_detailes.xlsx")
        raise


def GenResultsWorkbook(exempt_students:list[int]):
    workbook = xlsxwriter.Workbook("data/Filled_Groups.xlsx")
    worksheet = workbook.add_worksheet()

    format_header = workbook.add_format({'font_size': 12, 'bold': False, 'text_wrap': True, 'align': 'center', 
                                         'bg_color': '#BFBFBF', 'border':1, 'left':0, 'right':5, 'bottom':5 , 'top':5})
    format_header_first = workbook.add_format({'font_size': 12, 'bold': False, 'text_wrap': True, 'align': 'center', 
                                         'bg_color': '#BFBFBF', 'border':1, 'left':5, 'right':0, 'bottom':5 , 'top':5})
    format_header_last = workbook.add_format({'font_size': 12, 'bold': False, 'text_wrap': True, 'align': 'center', 
                                         'bg_color': '#BFBFBF', 'border':1, 'left':0, 'right':5, 'bottom':5 , 'top':5})

    format_surname = workbook.add_format({'align': 'center', 'border':1, 'left':5, 'right':0, 'bottom':0 , 'top':0})
    format_bottom_surname = workbook.add_format({'align': 'center', 'border':1, 'left':5, 'right':0, 'bottom':5 , 'top':0})
    format_center = workbook.add_format({'align': 'center', 'border':1, 'left':0, 'right':5, 'bottom':0 , 'top':0})
    format_bottom_center = workbook.add_format({'align': 'center', 'border':1, 'left':0, 'right':5, 'bottom':5 , 'top':0})
    format_jmbag = workbook.add_format({'num_format': '0000000000', 'align': 'center', 'border':1, 'left':0, 'right':5, 'bottom':0 , 'top':0})
    format_bottom_jmbag = workbook.add_format({'num_format': '0000000000', 'align': 'center', 'border':1, 'left':0, 'right':5, 'bottom':5 , 'top':0})
    
    worksheet.write("A1", "Prezime", format_header_first)
    worksheet.write("B1", "Ime", format_header)
    worksheet.write("C1", "Email", format_header)
    worksheet.write("D1", "JMBAG", format_header)
    worksheet.write("E1", "Korisničko ime", format_header)
    worksheet.write("F1", "Grupa", format_header_last)

    worksheet.set_row(0, 30)    # row 1 -> height 50px

    width1 = len("Prezime")+1
    width2 = len("Ime")+1
    width3 = len("Email")+1
    width4 = 12 # JMBAG
    width5 = len("Korisničko ime")+1
    width6 = len("Grupa")+1

    row: int = 2
    student: Student = None
    cours_participants_list: list[Student] = []

    for student in settings.cours_participants_result.values():
        cours_participants_list.append(student)

    locale.setlocale(locale.LC_COLLATE, "croatian")
    cours_participants_list.sort(key=lambda x: locale.strxfrm(x.surname))

    for student in cours_participants_list:
        if student is cours_participants_list[-1]: 
            format = format_bottom_surname
            format1 = format_bottom_center
            format2 = format_bottom_jmbag
        else: 
            format = format_surname
            format1 = format_center
            format2 = format_jmbag
        worksheet.write(f"A{row}", f"{student.surname}", format)
        worksheet.write(f"B{row}", f"{student.name}", format1)
        worksheet.write(f"C{row}", f"{student.email}", format1)
        worksheet.write(f"D{row}", student.jmbag, format2)
        worksheet.write(f"E{row}", f"{student.username}", format1)
        if student.jmbag in exempt_students:
            worksheet.write(f"F{row}", "Oslobođen", format1)
            groupstr = "Osloboden"
        elif hasattr(student, "group"):
            worksheet.write(f"F{row}", f"{student.group}", format1)
            groupstr = f"{student.group}"
        else:
            worksheet.write(f"F{row}", "Još nisu svrstani", format1)
            groupstr = "Jos nisu svrstani"

        if width1 < len(f"{student.surname}"):
            width1 = len(f"{student.surname}")+1

        if width2 < len(f"{student.name}"):
            width2 = len(f"{student.name}")+1
        
        if width3 < len(f"{student.email}"):
            width3 = len(f"{student.email}")+3
        
        if width4 < len(f"{student.jmbag}"):
            width4 = len(f"{student.jmbag}")+1
        
        if width5 < len(f"{student.username}"):
            width5 = len(f"{student.username}")+1

        if width6 < len(groupstr):
            width6 = len(groupstr)+1

        worksheet.set_row(row-1, 18)  # student rows -> height 30px
        
        row += 1
    
    worksheet.set_column(0, 0, width1)
    worksheet.set_column(1, 1, width2)
    worksheet.set_column(2, 2, width3)
    worksheet.set_column(3, 3, width4)
    worksheet.set_column(4, 4, width5)
    worksheet.set_column(5, 5, width6)

    worksheet.autofilter(0,5, len(cours_participants_list),5)

    workbook.close()