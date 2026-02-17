# VCF to Excel Converter

A simple Python script to convert a `.vcf` (vCard) file into an Excel `.xlsx` file.

## Requirements

- Python 3.x
- pandas
- openpyxl

Install required packages:

```bash
pip install pandas openpyxl
```

## Usage

Run the script from the command line:

```bash
python vcf_to_excel.py input.vcf -o output.xlsx
```

If you do not provide the `-o` option, the script will automatically create an Excel file with the same name as the input file.

Example:

```bash
python vcf_to_excel.py contacts.vcf
```

This will create:

```
contacts.xlsx
```

## Extracted Fields

The script extracts the following fields from the VCF file:

- Full Name
- Phone Numbers
- Emails
- Organization
- Address

## Notes

- Multiple phone numbers and emails are combined into a single cell separated by commas.
- The input file must be a valid `.vcf` file.

