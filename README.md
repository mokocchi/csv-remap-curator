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

  ## Interactive Docker version!

  You can run the dockerized version of the application, mounting the file you want to process as a volume like this:

  ```
  docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator --help

  docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator csv-info -i /data/yourfile.csv

  docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator get-columns -i /data/yourfile.csv
  ``` 

  where `/absolute/path/to/your/file` and `yourfile.csv` must be replaced with your path and filename.

