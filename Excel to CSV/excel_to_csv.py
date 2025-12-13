import pandas as pd
import sys
import os

    #excel_file: Path to the Excel file 
    #output_csv: Path to save the output CSV file
    #sheet_name: Name of the sheet to convert. If None, the first sheet is used

def convert_excel_to_csv(excel_file, output_csv, sheet_name=None):

    
    try:
        #Checks if the file exists
        if not os.path.exists(excel_file): 
            print(f"Error: The file '{excel_file}' does not exist.")
            return

        #Reads the Excel file
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file)

        # Converts the Excel file to CSV foormaat
        df.to_csv(output_csv, index=False)
        print(f"Successfully converted '{excel_file}' to '{output_csv}'.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python excel_to_csv.py <input_excel_file> <output_csv_file> [sheet_name]")
    else:
        input_excel_file = sys.argv[1]
        output_csv_file = sys.argv[2]
        sheet_name = sys.argv[3] if len(sys.argv) > 3 else None
        convert_excel_to_csv(input_excel_file, output_csv_file, sheet_name)
