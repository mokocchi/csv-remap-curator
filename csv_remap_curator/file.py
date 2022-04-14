import configparser
import csv
from pathlib import Path
from sys import stdin
from typing import Any, Dict, List, NamedTuple, Optional
from csv_remap_curator import FILE_READ_ERROR, PARSE_ERROR, SUCCESS, FILE_WRITE_ERROR

DEFAULT_OUTPUT_FILE_PATH = "output.csv"


class FileResponse(NamedTuple):
    column_list: List[Dict[str, Any]]
    error: int


class FileHandler:
    def __init__(self, input_file_path: Path, output_file_path: Optional[Path], delimiter: str, remap_file_path: Path) -> None:
        self._input_file_path = input_file_path
        self._output_file_path = output_file_path
        self._remap_file_path = remap_file_path
        self._delimiter = delimiter

    def read_columns(self) -> Optional[FileResponse]:
        try:
            with self._input_file_path.open("r") as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=self._delimiter, quoting=csv.QUOTE_MINIMAL)
                    line = reader.__next__()
                except Exception as e:
                    return FileResponse([], PARSE_ERROR)
        except OSError:
            return FileResponse([], FILE_READ_ERROR)
        if(not self._output_file_path):
            return FileResponse(line, SUCCESS)
        else:
            try:
                with self._output_file_path.open("w") as f:
                    try:
                        writer = csv.DictWriter(f, line)
                        writer.writeheader()
                        return FileResponse([], SUCCESS)
                    except Exception:
                        return FileResponse([], FILE_WRITE_ERROR)
            except OSError:
                return FileResponse([], FILE_WRITE_ERROR)
