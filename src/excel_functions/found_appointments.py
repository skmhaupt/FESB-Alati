from datetime import datetime
from gui.util import CopyAndRename
import xlsxwriter


def GenFoundAppointmentsWorkbook(appointments_all_can_join: list[tuple[datetime,datetime]], cours_name:str, cours_number:str, acad_year:int):
    try:
        workbook = xlsxwriter.Workbook("gui/group_finder/data/FoundAppointments.xlsx")
        worksheet = workbook.add_worksheet("Termini")

        header_format = workbook.add_format({'align': 'center', 'font_size': 12, 'bold': False})
        center_format = workbook.add_format({'align': 'center'})
        dates_format = workbook.add_format({'align': 'center', 'border':1, 'top':0, 'bottom':5, 'right':0, 'left':0})

        worksheet.write("B2", f"Dostupni termini za {cours_name} {cours_number}", header_format)
        
        ap_dates: dict[str,tuple[int,int]] = {}
        col = 0
        for appointment in appointments_all_can_join:
            date = appointment[0].date()
            date = f"{date}"
            ap_start = appointment[0].time()
            ap_end = appointment[1].time()
            if not date in ap_dates.keys():
                ap_dates[date] = (4,col)
                worksheet.write(3,col, date, dates_format)
                col+=1
            row = ap_dates[date][0]
            col2=ap_dates[date][1]
            worksheet.write(row,col2, f"{ap_start} - {ap_end}", center_format)
            row+=1
            ap_dates[date] = (row, col2)
        
        for _,col in ap_dates.values():
            worksheet.set_column(col, col, 20)

        workbook.close()

        CopyAndRename(srcpath="gui/group_finder/data/FoundAppointments.xlsx", dstname="dostupni_termini")

    except Exception:
        raise