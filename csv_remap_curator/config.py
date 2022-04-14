import configparser
import os
from pathlib import Path
import typer

from csv_remap_curator import (
    DIR_ERROR, FILE_ERROR, FILE_WRITE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path("/tmp")
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_app(db_path: str) -> int:
    """Initialize the application."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    output_file_code = _create_output_file(db_path)
    if output_file_code != SUCCESS:
        return output_file_code
    return SUCCESS

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError as err:
        print(err)
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError as err:
        print(err)
        return FILE_ERROR
    return SUCCESS

def _create_output_file(output_file_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"output_file": output_file_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return FILE_WRITE_ERROR
    return SUCCESS