# freelance-help-program
This software is designed to help freelancers calculate their payment based on hours worked. It takes an Excel file as input, where the start time is written in the first column and the end time is written in the second column. The software calculates the total time and the amount to be paid according to the hourly payment entered by the user.

## Installation

Layer the repository or download the code files.
Install the required dependencies by running the following command:
    pip install openpyxl
   
## Usage

1. Run the program by executing the following command:
 python calculate_payment.py

The program will open a graphical user interface (GUI) window.
Click the "Browse" button to select the Excel file containing the time values.
Enter the hourly rate in the appropriate input field.
Click the "Calculate" button to calculate the payment.
The program will display a message box with the total payment amount.
The modified Excel file with the calculated results will be saved as "modified_[original_file_name].xlsx".

Note: Make sure the Excel file has the correct format, with the start time in the first column and the end time in the second column.
