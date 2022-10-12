import openpyxl
import sys

csv_name = input("Name of the input CSV file with extension: ")
sep = input("Separator of the CSV file: ")
ename = input("Name of the output excel file with extension: ")
sname = input("Name of the output excel sheet: ")
try:
    workbook = openpyxl.load_workbook(ename)
    sheet = workbook.get_sheet_by_name(sname)

    file = open(csv_name, "r", encoding="utf-8")
except:
    print("Error: File not found")
    sys.exit()
excel_row = 1
excel_column = 1

for lines in file:

    lines = lines[:-1]
    lines = lines.split(sep)

    for dat in lines:

        sheet.cell(excel_row, excel_column).value = dat

        excel_column += 1

    excel_column = 1
    excel_row += 1


workbook.save(ename)
file.close()
