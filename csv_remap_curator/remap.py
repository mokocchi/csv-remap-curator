from pathlib import Path
from typing import Any, Dict, List, Optional

from csv_remap_curator import FILE_ERROR, FILE_READ_ERROR, FILE_WRITE_ERROR, OS_ERROR, SUCCESS, __app_name__
from csv_remap_curator.file import FileHandler, FileResponse, InfoResponse, StatusResponse


class Remapper:
    def __init__(self, input_file_path:Path, input_file_encoding: Optional[str], output_file_path: Optional[Path], output_file_encoding: Optional[str], delimiter: str, remap_file_path: Optional[str], decimal_point: str) -> None:
        self.__file_handler = FileHandler(input_file_path, input_file_encoding, output_file_path, output_file_encoding, delimiter, remap_file_path, decimal_point)
    
    def get_columns(self) -> FileResponse:
      """Return the columns of the input file"""
      return self.__file_handler.read_columns()
    
    def get_info(self) -> InfoResponse:
      """Return info about the input file"""
      return self.__file_handler.get_info()

    def remap_columns(self) -> StatusResponse:
      """Remap the columns of the input file following the remap file"""
      return self.__file_handler.remap_columns()
    
    def preprocess_csv(self) -> StatusResponse:
      """Preprocess the input file"""
      return self.__file_handler.preprocess_csv()
    
    def sample_csv(self, sample_start: int, sample_count: int) -> StatusResponse:
      """Sample a csv file a number of rows from the selected row"""
      return self.__file_handler.sample_csv(sample_start, sample_count)