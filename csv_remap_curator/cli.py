from pathlib import Path
from typing import Optional

import typer

from csv_remap_curator import ERRORS, __app_name__, __version__, config, remap

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
def init(
    output_file_path: str = typer.Option(
        str(remap.DEFAULT_OUTPUT_FILE_PATH),
        "--output-file",
        "-o",
        prompt="output file name",
    ),
) -> None:
    """Initialize the output file."""
    app_init_error = config.init_app(output_file_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    output_file_init_error = remap.init_output_file(Path(output_file_path))
    if output_file_init_error:
        typer.secho(
            f'Creating output file failed with "{ERRORS[output_file_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"The output file is {output_file_path}", fg=typer.colors.GREEN)
