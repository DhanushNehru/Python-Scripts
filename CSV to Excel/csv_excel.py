import openpyxl
import os

# Get the CSV and Excel file names from the user
csv_name = input("Name of the input CSV file with extension: ")
sep = input("Separator of the CSV file: ")
excel_name = input("Name of the output excel file with extension: ")
sheet_name = input("Name of the output excel sheet: ")

# Load the CSV file
if os.path.exists(excel_name):
    workbook = openpyxl.load_workbook(excel_name)
    sheet = workbook[sheet_name] if sheet_name in workbook.sheetnames else workbook.create_sheet(sheet_name)
else:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name

# Write the CSV data to the Excel sheet
try:
    with open(csv_name, "r", encoding="utf-8") as file:
        excel_row = 1
        for line in file:
            data = line.strip().split(sep)
            excel_column = 1
            for value in data:
                sheet.cell(row=excel_row, column=excel_column, value=value)
                excel_column += 1
            excel_row += 1

    # Save the Excel file
    workbook.save(excel_name)

except FileNotFoundError:
    print("Error: The CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")