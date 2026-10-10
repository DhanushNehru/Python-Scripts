# API Response Comparator

A command-line utility for comparing two JSON files, typically used to identify differences in API responses. It highlights keys added, removed, and values changed between two JSON documents, supporting nested objects and arrays.

## Prerequisites

- Python 3.6 or higher.
- Standard Python libraries (`json`, `argparse`, `sys`). No external dependencies required.

## How to Run

You can run the script from the command line by passing the paths to the two JSON files you want to compare:

```bash
python compare_json.py old.json new.json
```

## Command-Line Arguments

- `old_json`: The path to the first (old/original) JSON file.
- `new_json`: The path to the second (new/updated) JSON file.
- `-h`, `--help`: Show the help message and exit.

## Exit Codes

- `0`: No differences found. The JSON files are identical.
- `1`: Differences found between the JSON files.
- `2`: Error during execution (e.g., file not found, malformed JSON, invalid arguments).

## Example

**old.json**
```json
{
  "name": "Alice",
  "age": 25,
  "address": {
    "city": "Jeddah"
  }
}
```

**new.json**
```json
{
  "name": "Alice",
  "age": 26,
  "email": "alice@example.com",
  "address": {
    "city": "Riyadh"
  }
}
```

**Command**
```bash
python compare_json.py old.json new.json
```

**Output**
```text
Differences found:
- address.city: changed from "Jeddah" to "Riyadh"
- age: changed from 25 to 26
- email: added with value "alice@example.com"
```

## Running the Tests

To ensure the utility works as expected, a suite of unit tests is included. Run the tests with the following command:

```bash
python -m unittest tests/test_compare_json.py
```
