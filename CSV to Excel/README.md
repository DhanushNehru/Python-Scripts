# Explanation of Modifications

**Support for Multiple CSV Files:**

Modification: We now accept multiple CSV files, split by commas, in the csv_files list.

Sheet Name: For each CSV file, a new sheet is created, named after the CSV file (without the extension).

Loop: We loop over each CSV file in csv_files and process it individually.

**Automatic CSV Header Detection and Formatting:**

Modification: The first row of each CSV file is detected as the header.

Formatting: The header row is formatted with bold text (Font(bold=True)) and a yellow background (PatternFill).

Flag: A header_detected flag ensures that formatting is only applied to the first row

**Handling Empty or Invalid Files:**

Error handling remains in place for file not found and general exceptions.

#Thank You