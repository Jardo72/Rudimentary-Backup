from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import datetime
from os import makedirs
from os.path import join

from rich.console import Console
from rich.table import Table

from archiver import Archiver, ArchiveInfo
from config import read_configuration, Configuration


def epilog() -> str:
    ...


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Rudimentary Backup Tool", epilog=epilog(), formatter_class=RawTextHelpFormatter)

    # positional mandatory arguments
    parser.add_argument(
        "config_file",
        help="the name of the configuration YAML file"
    )

    # optional arguments
    parser.add_argument(
        "-o", "--output-html",
        dest="output_html_file",
        default=None,
        help="the optional name of an HTML output file the report is to be written to"
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def current_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def print_summary(archive_info_list: list[ArchiveInfo], console: Console) -> None:
    table = Table(title="Summary", show_lines=True)

    table.add_column("Target", justify="left")
    table.add_column("Archived Files", justify="right")
    table.add_column("Archived Bytes", justify="right")
    table.add_column("Ignored Files", justify="right")
    table.add_column("Archive Size", justify="right")
    table.add_column("Status", justify="center")
    
    for archive_info in archive_info_list:
        table.add_row(
            archive_info.target.description,
            str(archive_info.archived_file_count),
            str(archive_info.archived_byte_count),
            str(archive_info.ignored_file_count),
            str(archive_info.archive_size),
            archive_info.status.name
        )

    console.print(table)


def create_backup(configuration: Configuration, console: Console) -> None:
    target_count = len(configuration.targets)
    archive_info_list = []
    destination_dir = join(configuration.destination_dir, current_timestamp())
    makedirs(destination_dir, exist_ok=True)
    with console.status("[bold][blue]Archiving target...[/blue][bold]"):
        for index, target in enumerate(configuration.targets):
            archiver = Archiver(target, configuration.temp_dir, destination_dir)
            archive_info = archiver.create_archive()
            archive_info_list.append(archive_info)
            console.print(f"Target [green][bold]{target.description}[/green][/bold] ({index + 1}/{target_count}) archived")
        console.print("[bold][green]All targets archived.[/bold][/green]")
    print_summary(archive_info_list, console)


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    console = Console(record=True)
    console.print()
    try:
        configuration = read_configuration(cmd_line_args.config_file)
        create_backup(configuration, console)
    except Exception as e:
        console.print_exception(show_locals=False)
    if cmd_line_args.output_html_file:
        console.save_html(cmd_line_args.output_html_file)


if __name__ == "__main__":
    main()
