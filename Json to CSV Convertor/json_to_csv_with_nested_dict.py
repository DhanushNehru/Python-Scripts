import json
import csv

def json_to_csv(json_data, csv_file, mapping=None):

  if isinstance(json_data, list):
    # Flatten nested JSON structures.
    json_data = [flatten_json(obj) for obj in json_data]

  # Get the column headers from the mapping or from the JSON data itself.
  column_headers = mapping or json_data[0].keys()

  # Write the CSV file.
  with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(column_headers)
    for row in json_data:
      # Convert nested values to strings.
      row_values = [str(row.get(column, "")) for column in column_headers]
      writer.writerow(row_values)

def flatten_json(obj):

  flattened = {}
  for key, value in obj.items():
    if isinstance(value, dict):
      flattened.update(flatten_json(value))
    elif isinstance(value, list):
      for item in value:
        flattened["{}.{}".format(key, item)] = item
    else:
      flattened[key] = value
  return flattened

# sample mapping if needed
mapping = {
    "name": "Name",
    "status": "Status",
    "date": "Date",
    "author": "Author",
    "probability": "Probability",
    "result": "Result",
    "final_status": "Final Status",
    "connected.run_again": "Run Again",
    "connected.next_test": "Next Test",
    "connected.next_test_status": "Next Test Status"
}


def main():
  # Load the JSON data.
  with open("json_data.json", "r") as json_file:
    json_data = json.load(json_file)

  # Convert the JSON data to CSV format.
  json_to_csv(json_data, "csv_data.csv")

if __name__ == "__main__":
  main()
