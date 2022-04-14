# csv-remap-curator
A command line application for remapping and curating csv files

## Available commands
- `read-columns`

  ```
  Usage: csv_remap_curator read-columns [OPTIONS]

  
    Read the columns of the input file.
  
  Options:
  
    -i, --input-file TEXT   Input file
  
    -o, --output-file TEXT  Output file
  
    -d, --delimiter TEXT    Column delimiter
  
    --help                  Show this message and exit.
  ```

  - `csv-info`
  ```
  Usage: csv_remap_curator csv-info [OPTIONS]

  Information about the input file.

  Options:
    -i, --input-file TEXT  Input file
    -d, --delimiter TEXT   Column delimiter
    --help                 Show this message and exit.
  ```