from pathlib import Path
from typing import Any, Dict, List, Optional

from csv_remap_curator import FILE_ERROR, FILE_READ_ERROR, FILE_WRITE_ERROR, OS_ERROR, SUCCESS, __app_name__
from csv_remap_curator.file import FileHandler


class Remapper:
    def __init__(self, input_file_path:Path, output_file_path: Optional[Path], delimiter: str, remap_file_path) -> None:
        self.__file_handler = FileHandler(input_file_path, output_file_path, delimiter, remap_file_path)
    
    def get_columns(self) -> List[Dict[str, Any]]:
      """Return the columns of the input file"""
      return self.__file_handler.read_columns()
