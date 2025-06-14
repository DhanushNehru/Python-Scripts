# README.md

# CSV to NDJSON Converter

This Python script converts a CSV file located in this folder into an NDJSON file saved in the same folder.

## What is NDJSON?

NDJSON (Newline Delimited JSON) is a convenient format for streaming JSON objects, where each line is a valid JSON object.  
It’s widely used in data pipelines and tools such as **Google Cloud BigQuery**, **ElasticSearch**, and many other data processing platforms.

## How to use

1. Place your CSV file in this folder.
2. Make sure you have Python 3 installed.
3. Run the script from this folder with:

   ```bash
   python csv_to_ndjson.py input.csv output.ndjson


#### Example 
If you have a CSV file like this:

```csv
name,age,city
Alice,30,New York
Bob,25,Los Angeles
```

The output NDJSON will be:

```json
{"name":"Alice","age":"30","city":"New York"}
{"name":"Bob","age":"25","city":"Los Angeles"}
```

Feel free to modify or extend it as needed.
