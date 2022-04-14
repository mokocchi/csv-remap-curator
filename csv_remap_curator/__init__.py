__app_name__ = "csv_remap_curator"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    FILE_WRITE_ERROR,
    FILE_READ_ERROR,
    PARSE_ERROR,
    OS_ERROR
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    FILE_WRITE_ERROR: "output file error",
    FILE_READ_ERROR: "input file error",
    PARSE_ERROR: "the file is not a valid csv file",
    OS_ERROR: "operating system permissions error"
}
