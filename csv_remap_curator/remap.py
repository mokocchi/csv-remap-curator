
import configparser
import os
from pathlib import Path

from csv_remap_curator import FILE_ERROR, FILE_WRITE_ERROR, OS_ERROR, SUCCESS, __app_name__

DEFAULT_OUTPUT_FILE_PATH = "output.csv"

def get_output_file_path(config_file: Path) -> Path:
    """Return the current path to the output file"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["output_file"])

def init_output_file(file_path: Path) -> int:
    """Create the output file."""
    try:
        file_path.write_text("")
        return SUCCESS
    except OSError:
        return FILE_WRITE_ERROR