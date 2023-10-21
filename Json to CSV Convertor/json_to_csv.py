import json
import csv

def json_to_csv(input_json_file, output_csv_file):
    try:
        # Read JSON data from input file using utf-8-sig encoding to handle BOM
        with open(input_json_file, 'r', encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        # Get the keys from the first JSON object to use as column headers
        headers = list(data[0].keys())

        # Write CSV data to output file
        with open(output_csv_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)

            # Write column headers to CSV file
            writer.writeheader()

            # Write JSON data to CSV file
            for row in data:
                writer.writerow(row)
        
        print(f"Conversion from JSON to CSV completed successfully. CSV file saved as {output_csv_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
input_json_file = 'path_to_input.json'
output_csv_file = 'path_to_output.csv'

json_to_csv(input_json_file, output_csv_file)
