from labgenpackage.classes import Student

import gui.settings as settings
import xlsxwriter, logging

def GenScraperDetailesWorkbook(csvMissing:list[Student], csvEmpty:list[Student]):
    try:
        workbook = xlsxwriter.Workbook("data/Student_schedules_Error_detailes.xlsx")
        worksheet = workbook.add_worksheet()

        merge_format = workbook.add_format({"border":1, "bottom":5, "align": "center"})

        worksheet.write("A2", "Ime i prezime")
        worksheet.write("B2", "JMBAG")
        worksheet.write("C2", "E-Mail")

        worksheet.write("E2", "Ime i prezime")
        worksheet.write("F2", "JMBAG")
        worksheet.write("G2", "E-Mail")
        
        width1 = len("Ime i prezime")+1
        width2 = len("JMBAG")+1
        width3 = len("E-Mail")+1
        row: int = 3
        for student in csvMissing:
            worksheet.write(f"A{row}", f"{student.fullname}")
            if width1 < len(f"{student.fullname}"):
                width1 = len(f"{student.fullname}")+1

            worksheet.write(f"B{row}", f"{student.jmbag}")
            if width2 < len(f"{student.jmbag}"):
                width2 = len(f"{student.jmbag}")+1

            worksheet.write(f"C{row}", f"{student.email}")
            if width3 < len(f"{student.email}"):
                width3 = len(f"{student.email}")+1

            row += 1

        worksheet.set_column(0, 0, width1)
        worksheet.set_column(1, 1, width2)
        worksheet.set_column(2, 2, width3)
        worksheet.merge_range("A1:C1", "Studenti kojima nije uspjesno preuzet raspored", merge_format)
        
        width1 = len("Ime i prezime")+1
        width2 = len("JMBAG")+1
        width3 = len("E-Mail")+1
        row: int = 3
        for student in csvEmpty:
            #worksheet.write(f"C{row}", f"{student}")
            worksheet.write(f"E{row}", f"{student.fullname}")
            if width1 < len(f"{student.fullname}"):
                width1 = len(f"{student.fullname}")+1

            worksheet.write(f"F{row}", f"{student.jmbag}")
            if width2 < len(f"{student.jmbag}"):
                width2 = len(f"{student.jmbag}")+1

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


def GenResultsWorkbook():
    workbook = xlsxwriter.Workbook("data/Filled_Groups.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write("A1", "Prezime")
    worksheet.write("B1", "Ime")
    worksheet.write("C1", "Email")
    worksheet.write("D1", "ID broj")
    worksheet.write("E1", "Korisničko ime")
    worksheet.write("F1", "Grupa")

    width1 = len("Prezime")+1
    width2 = len("Ime")+1
    width3 = len("Email")+1
    width4 = len("ID broj")+1
    width5 = len("Korisničko ime")+1
    width6 = len("Grupa")+1

    row: int = 2
    student: Student = None
    for student in settings.cours_participants_result.values():
        worksheet.write(f"A{row}", f"{student.surname}")
        worksheet.write(f"B{row}", f"{student.name}")
        worksheet.write(f"C{row}", f"{student.email}")
        worksheet.write(f"D{row}", f"{student.jmbag}")
        worksheet.write(f"E{row}", f"{student.username}")
        if hasattr(student, "group"):
            worksheet.write(f"F{row}", f"{student.group}")
            groupstr = f"{student.group}"
        else:
            worksheet.write(f"F{row}", "Jos nisu svrstani")
            groupstr = "Jos nisu svrstani"

        if width1 < len(f"{student.surname}"):
            width1 = len(f"{student.surname}")+1

        if width2 < len(f"{student.name}"):
            width2 = len(f"{student.name}")+1
        
        if width3 < len(f"{student.email}"):
            width3 = len(f"{student.email}")+1
        
        if width4 < len(f"{student.jmbag}"):
            width4 = len(f"{student.jmbag}")+1
        
        if width5 < len(f"{student.username}"):
            width5 = len(f"{student.username}")+1

        if width6 < len(groupstr):
            width6 = len(groupstr)+1
        
        worksheet.set_column(0, 0, width1)
        worksheet.set_column(1, 1, width2)
        worksheet.set_column(2, 2, width3)
        worksheet.set_column(3, 3, width4)
        worksheet.set_column(4, 4, width5)
        worksheet.set_column(5, 5, width6)

        row += 1
    
    workbook.close()