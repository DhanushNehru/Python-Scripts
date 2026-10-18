
import sqlite3
import csv
import os


def sqlite_to_csv(database_path, output_folder="csv_output"):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Get all table names
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
        """)

        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        # Export each table to its own CSV file
        for (table_name,) in tables:
            # Safely quote the table name
            quoted_name = '"' + table_name.replace('"', '""') + '"'

            cursor.execute(f"SELECT * FROM {quoted_name}")

            # Get column names
            column_names = [column[0] for column in cursor.description]

            # Create a CSV file for this table
            file_path = os.path.join(
                output_folder, f"{table_name}.csv"
            )

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(cursor)

            print(f"Exported '{table_name}' -> {file_path}")

        print("\nConversion completed!")

    finally:
        connection.close()


if __name__ == "__main__":
    database = input("Enter SQLite database path: ").strip()
    sqlite_to_csv(database)
