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
)) -> None:
    """Read the columns of the input file."""
    remapper = get_remapper(
        input_file_path, output_file_path, delimiter if delimiter else ",")
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


def get_remapper(input_file_path: Optional[str], output_file_path: Optional[str], delimiter: Optional[str] = ",", remap_file_path: Optional[str] = None) -> remap.Remapper:
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
                                      Path(
                    output_file_path) if output_file_path else None,
                    delimiter,
                    Path(
                    remap_file_path) if remap_file_path else None,)
