__app_name__ = "csv_remap_curator"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
) = range(3)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
}
