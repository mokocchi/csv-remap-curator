__app_name__ = "csv_remap_curator"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    FILE_WRITE_ERROR,
    OS_ERROR
) = range(5)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    FILE_WRITE_ERROR: "output file error",
    OS_ERROR: "operating system permissions error"
}
