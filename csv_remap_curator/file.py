import csv
from pathlib import Path
import subprocess
from sys import stdin
import sys
from time import time
from typing import Any, Dict, List, NamedTuple, Optional
from pyarrow import csv as pycsv
import pyarrow as pa
from ray.data.datasource import BlockWritePathProvider

import ray

from csv_remap_curator import FILE_READ_ERROR, PARSE_ERROR, REMAP_FILE_ERROR, REMAP_FILE_PARSE_ERROR, REMAPPING_ERROR, SUCCESS, FILE_WRITE_ERROR

import yaml
from yaml.loader import SafeLoader

DEFAULT_OUTPUT_FILE_PATH = "output.csv"


class FileResponse(NamedTuple):
    column_list: List[Dict[str, Any]]
    error: int


class InfoResponse(NamedTuple):
    info: Dict[str, Any]
    error: int


class StatusResponse(NamedTuple):
    status: Dict[str, Any]
    error: int


class CustomBlockWritePathProvider(BlockWritePathProvider):
    """Custom block write path provider implementation that writes each
    dataset block out to a file of the form:
    {base_path}/{output_file}_{block_index}.{file_format}
    """
    def __init__(self, output_file: str) -> None:
        super().__init__()
        self._output_file = output_file


    def _get_write_path_for_block(
            self,
            base_path: str,
            **kwargs) -> str:
        suffix = f"{self._output_file}"
        return f"{base_path}/{suffix}"

class FileHandler:
    def __init__(self, input_file_path: Path, input_file_encoding: Optional[str], output_file_path: Optional[Path], output_file_encoding: Optional[str], delimiter: str, remap_file_path: Optional[Path], decimal_point: str) -> None:
        self._input_file_path = input_file_path
        self._input_file_encoding = input_file_encoding
        self._output_file_path = output_file_path
        self._output_file_encoding = output_file_encoding
        self._remap_file_path = remap_file_path
        self._delimiter = delimiter
        self._decimal_point = decimal_point

    def read_columns(self) -> Optional[FileResponse]:
        try:
            with self._input_file_path.open("r", encoding=self._input_file_encoding) as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=self._delimiter, quoting=csv.QUOTE_MINIMAL)
                    line = reader.fieldnames
                except Exception as e:
                    print(e)
                    return FileResponse([], PARSE_ERROR)
        except OSError:
            return FileResponse([], FILE_READ_ERROR)
        if(not self._output_file_path):
            return FileResponse(line, SUCCESS)
        else:
            try:
                with self._output_file_path.open("w", encoding=self._output_file_encoding) as f:
                    try:
                        writer = csv.DictWriter(f, line)
                        writer.writeheader()
                        return FileResponse([], SUCCESS)
                    except Exception:
                        return FileResponse([], FILE_WRITE_ERROR)
            except OSError:
                return FileResponse([], FILE_WRITE_ERROR)

    def get_info(self) -> InfoResponse:
        try:
            with self._input_file_path.open("r", encoding=self._input_file_encoding) as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=self._delimiter, quoting=csv.QUOTE_MINIMAL)
                    line = reader.fieldnames
                    row_count = subprocess.check_output(
                        ['wc', '-l', self._input_file_path]).decode(sys.stdout.encoding).split()[0]
                    return InfoResponse({
                        "header_count": len(line),
                        "row_count": row_count
                    }, SUCCESS)
                except Exception as e:
                    return InfoResponse([], PARSE_ERROR)
        except OSError:
            return InfoResponse([], FILE_READ_ERROR)

    def remap_columns(self) -> Optional[StatusResponse]:
        try:
            with self._remap_file_path.open("r") as f:
                try:
                    mapping = yaml.load(f, Loader=SafeLoader)
                except Exception as e:
                    return StatusResponse("", REMAP_FILE_PARSE_ERROR)
        except OSError:
            return StatusResponse("", REMAP_FILE_ERROR)
        else:
            return process_file(mapping, self._input_file_path, self._output_file_path)

    def preprocess_csv(self) -> Optional[StatusResponse]:
        try:
            with self._input_file_path.open("r", encoding=self._input_file_encoding) as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=self._delimiter, quoting=csv.QUOTE_MINIMAL)
                    line = reader.fieldnames
                    try:
                        with self._output_file_path.open("w") as f:
                            try:
                                writer = csv.DictWriter(f, line)
                                writer.writeheader()
                                for row in reader:
                                    writer.writerow(row)
                                return StatusResponse("OK", SUCCESS)
                            except Exception as e:
                                return StatusResponse("", FILE_WRITE_ERROR)
                    except OSError:
                        return StatusResponse("", FILE_WRITE_ERROR)
                except Exception as e:
                    return StatusResponse("", PARSE_ERROR)
        except OSError:
            return StatusResponse("", FILE_READ_ERROR)
        
    def sample_csv(self, sample_start: int, sample_count: int) -> Optional[StatusResponse]:
        try:
            with self._input_file_path.open("r", encoding=self._input_file_encoding) as f:
                try:
                    reader = csv.DictReader(
                        f, delimiter=self._delimiter, quoting=csv.QUOTE_MINIMAL)
                    line = reader.fieldnames
                    try:
                        with self._output_file_path.open("w") as f:
                            try:
                                writer = csv.DictWriter(f, line)
                                writer.writeheader()
                                i = 0
                                sample_start = int(sample_start)
                                sample_count = int(sample_count)
                                sample_end = sample_start + sample_count
                                for row in reader:
                                    if(i < sample_start):
                                        i += 1
                                    elif (i < sample_end):
                                        writer.writerow(row)
                                        i += 1
                                    else:
                                        break
                                return StatusResponse("OK", SUCCESS)
                            except Exception as e:
                                print(e)
                                return StatusResponse("", FILE_WRITE_ERROR)
                    except OSError:
                        return StatusResponse("", FILE_WRITE_ERROR)
                except Exception as e:
                    return StatusResponse("", PARSE_ERROR)
        except OSError:
            return StatusResponse("", FILE_READ_ERROR)


def process_file(mapping: Dict[str, Any], input_file_path: str, output_file_path: str):
    decimal_point = mapping.get("decimal_point")
    delimiter = mapping.get("delimiter")
    input_file_encoding = mapping.get("encoding")
    column_types = {}
    include_columns = []
    for column in mapping.get("mappings"):
        include_columns.append(column.get("name"))
        if column.get("type") == "float":
            col_type = pa.float32()
        elif column.get("type") == "text":
            col_type = pa.string()
        elif column.get("type") == "integer":
            col_type = pa.int32()
        elif column.get("type") == "date":
            col_type = pa.date32()
        else:
            col_type = None
        column_types[column.get("name")] = col_type
    start = time()
    try:
        ds = ray.data.read_csv(
            str(Path(input_file_path)),
            read_options=pycsv.ReadOptions(encoding=input_file_encoding, column_names=[]),
            convert_options=pycsv.ConvertOptions(decimal_point=decimal_point, column_types=column_types, include_columns=include_columns),
            parse_options=pycsv.ParseOptions(delimiter=delimiter, invalid_row_handler=invalid_row_callback))
        print(time() - start)
        start = time()
        ds.write_csv(path=str(Path(output_file_path).parent), block_path_provider=CustomBlockWritePathProvider(output_file_path))
        print(time() - start)
        return FileResponse([], SUCCESS)
    except Exception as e:
        print(e)
        return FileResponse([], REMAPPING_ERROR)

def invalid_row_callback(row):
    print("PARSE ERROR")
    print(row)
    print("PARSE ERROR END")