# csv-remap-curator
A command line application for remapping and curating csv files

## Running the module

```
python -m csv_remap_curator
```

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

- `preprocess-file`

  ```
  Usage: csv_remap_curator preprocess-file [OPTIONS]

    Preprocess a csv file with utf-8 encoding and comma delimiter

  Options:
    -i, --input-file TEXT           Input file
    -d, --delimiter TEXT            Column delimiter
    -o, --output-file TEXT          Output file
    -I, --input-file-encoding TEXT  Encoding of the input file
    -O, --output-file-encoding TEXT
                                    Encoding of the output file
    --help                          Show this message and exit.
  ```
- `sample-file`
  ```
  Usage: csv_remap_curator sample-file [OPTIONS]

  Sample a csv file a number of rows from the selected row

  Options:
    -i, --input-file TEXT           Input file
    -d, --delimiter TEXT            Column delimiter
    -o, --output-file TEXT          Output file
    -I, --input-file-encoding TEXT  Encoding of the input file
    -O, --output-file-encoding TEXT
                                    Encoding of the output file
    -s, --sample-start TEXT         Start row of the sample
    -c, --sample-count TEXT         Row count of the sample
    --help                          Show this message and exit.
  ```

- `remap-columns`
  ```
  Usage: csv_remap_curator remap-columns [OPTIONS]

  Remap fields following a remap file

  Options:
    -i, --input-file TEXT   Input file
    -o, --output-file TEXT  Output file
    -r, --remap-file TEXT   Remap file
    --help                  Show this message and exit.
  ```

## Interactive Docker version!

You can run the dockerized version of the application, mounting the file you want to process as a volume like this:

`--help`

```
docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator --help
```

`csv-info`

```
  docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator csv-info -i /data/yourfile.csv
```

`read-columns`

```
  docker run -it --name csv-remap-curator --mount type=bind,source=/absolute/path/to/file,target=/data,readonly --rm csv-remap-curator python -m csv_remap_curator get-columns -i /data/yourfile.csv
  ``` 

  where `/absolute/path/to/your/file` and `yourfile.csv` must be replaced with your path and filename.

