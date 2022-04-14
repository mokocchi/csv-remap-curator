from pathlib import Path
from sys import stdin
from typing import Optional

import typer

from csv_remap_curator import ERRORS, __app_name__, __version__, config, file, remap

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def read_columns(input_file_path: Optional[str] = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Input file",
        is_eager=True,
    ),
    output_file_path: Optional[str] = typer.Option(
        None,
        "--output-file",
        "-o",
        help="Output file",
        is_eager=True,
),
    delimiter: Optional[str] = typer.Option(
        None,
        "--delimiter",
        "-d",
        help="Column delimiter",
        is_eager=True,
),
    input_file_encoding: Optional[str] = typer.Option(
        None,
        "--input-file-encoding",
        "-I",
        help="Encoding of the input file",
        is_eager=True,
),
    output_file_encoding: Optional[str] = typer.Option(
        None,
        "--output-file-encoding",
        "-O",
        help="Encoding of the output file",
        is_eager=True,
)
) -> None:
    """Read the columns of the input file."""
    remapper = get_remapper(
        input_file_path, input_file_encoding, output_file_path, output_file_encoding, delimiter)
    if remapper:
        column_list, error = remapper.get_columns()
        if error:
            typer.secho(
                f'Reading csv columns failed with "{ERRORS[error]}"', fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            if(not output_file_path):
                headers = "|".join(column_list)
                typer.secho(headers, fg=typer.colors.BLUE, bold=True)
                typer.secho("-" * len(headers), fg=typer.colors.BLUE)


@app.command()
def csv_info(input_file_path: Optional[str] = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Input file",
        is_eager=True,
    ),
    delimiter: Optional[str] = typer.Option(
        None,
        "--delimiter",
        "-d",
        help="Column delimiter",
        is_eager=True,
),
    input_file_encoding: Optional[str] = typer.Option(
        None,
        "--input-file-encoding",
        "-I",
        help="Encoding of the input file",
        is_eager=True,

)) -> None:
    """Information about the input file."""
    remapper = get_remapper(
        input_file_path, input_file_encoding, None, None, delimiter if delimiter else ",")
    if remapper:
        info, error = remapper.get_info()
        if error:
            typer.secho(
                f'Reading csv info failed with "{ERRORS[error]}"', fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f'Header count: {info["header_count"]}', fg=typer.colors.BLUE
            )
            typer.secho(
                f'Row count: {info["row_count"]}', fg=typer.colors.BLUE
            )


@app.command()
def remap_columns(input_file_path: Optional[str] = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Input file",
        is_eager=True,
    ),
    delimiter: Optional[str] = typer.Option(
        None,
        "--delimiter",
        "-d",
        help="Column delimiter",
        is_eager=True,
), output_file_path: Optional[str] = typer.Option(
        None,
        "--output-file",
        "-o",
        help="Output file",
        is_eager=True,
),
    remap_file_path: Optional[str] = typer.Option(
        None,
        "--remap-file",
        "-r",
        help="Remap file",
        is_eager=True,
),
    input_file_encoding: Optional[str] = typer.Option(
        None,
        "--input-file-encoding",
        "-I",
        help="Encoding of the input file",
        is_eager=True,
),
    output_file_encoding: Optional[str] = typer.Option(
        None,
        "--output-file-encoding",
        "-O",
        help="Encoding of the output file",
        is_eager=True,
)) -> None:
    """Remap fields following a remap file"""
    if(not output_file_path):
        typer.secho(
            'Output file not specified',
            fg=typer.colors.RED,
        )
    elif(not remap_file_path):
        typer.secho(
            'Remap file not specified',
            fg=typer.colors.RED,
        )
    else:
        if(not Path(remap_file_path).exists()):
            typer.secho(
                'Remap file not found',
                fg=typer.colors.RED,
            )
        else:
            remapper = get_remapper(
                input_file_path, input_file_encoding,
                output_file_path, output_file_encoding,
                delimiter if delimiter else ",", remap_file_path)
            if remapper:
                info, error = remapper.remap_columns()
                if error:
                    typer.secho(
                        f'Mapping csv failed with "{ERRORS[error]}"', fg=typer.colors.RED
                    )
                    raise typer.Exit(1)
                else:
                    pass


@app.command()
def preprocess_file(input_file_path: Optional[str] = typer.Option(
        None,
        "--input-file",
        "-i",
        help="Input file",
        is_eager=True,
    ),
    delimiter: Optional[str] = typer.Option(
        None,
        "--delimiter",
        "-d",
        help="Column delimiter",
        is_eager=True,
), output_file_path: Optional[str] = typer.Option(
        None,
        "--output-file",
        "-o",
        help="Output file",
        is_eager=True,
),
    input_file_encoding: Optional[str] = typer.Option(
        None,
        "--input-file-encoding",
        "-I",
        help="Encoding of the input file",
        is_eager=True,
),
    output_file_encoding: Optional[str] = typer.Option(
        None,
        "--output-file-encoding",
        "-O",
        help="Encoding of the output file",
        is_eager=True,
)) -> None:
    """Remap fields following a remap file"""
    if(not output_file_path):
        typer.secho(
            'Output file not specified',
            fg=typer.colors.RED,
        )
    else:
        remapper = get_remapper(
            input_file_path, input_file_encoding,
            output_file_path, output_file_encoding,
            delimiter if delimiter else ",")
        if remapper:
            info, error = remapper.preprocess_csv()
            if error:
                typer.secho(
                    f'Preprocess csv failed with "{ERRORS[error]}"', fg=typer.colors.RED
                )
                raise typer.Exit(1)
            else:
                pass


def get_remapper(input_file_path: Optional[str], input_file_encoding: Optional[str], output_file_path: Optional[str], output_file_encoding: Optional[str], delimiter: Optional[str] = ",", remap_file_path: Optional[str] = None) -> remap.Remapper:
    if(output_file_path):
        if not Path(output_file_path).exists():
            Path.touch(Path(output_file_path))
    if(not input_file_path):
        typer.secho(
            'Input file not specified',
            fg=typer.colors.RED,
        )
    else:
        if(not Path(input_file_path).exists()):
            typer.secho(
                'Input file not found',
                fg=typer.colors.RED,
            )
        else:
            if(remap_file_path and not Path(remap_file_path).exists()):
                typer.secho(
                    'Remap file not found',
                    fg=typer.colors.RED,
                )
            else:
                return remap.Remapper(Path(input_file_path),
                                      input_file_encoding,
                                      Path(
                    output_file_path) if output_file_path else None,
                    output_file_encoding,
                    delimiter if delimiter else ",",
                    Path(
                    remap_file_path) if remap_file_path else None,)
