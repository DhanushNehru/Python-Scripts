# csv_to_ndjson.py
import csv
import json
import sys
import os


def csv_to_ndjson(csv_filename, ndjson_filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(base_dir, csv_filename)
    ndjson_path = os.path.join(base_dir, ndjson_filename)

    try:
        with (
            open(csv_path, mode="r", encoding="utf-8") as f_csv,
            open(ndjson_path, mode="w", encoding="utf-8") as f_ndjson,
        ):
            reader = csv.DictReader(f_csv)
            for row in reader:
                f_ndjson.write(
                    json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                )

        print(f"Successfully converted '{csv_path}' to '{ndjson_path}'")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_ndjson.py input.csv output.ndjson")
    else:
        csv_file = sys.argv[1]
        ndjson_file = sys.argv[2]
        csv_to_ndjson(csv_file, ndjson_file)
