from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from rich.console import Console
from rich.table import Table

from archiver import Archiver, ArchiveInfo
from config import read_configuration


def epilog() -> str:
    ...


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Rudimentary Backup Tool", epilog=epilog(), formatter_class=RawTextHelpFormatter)

    # positional mandatory arguments
    parser.add_argument(
        "config_file",
        help="the name of the configuration YAML file"
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


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


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    configuration = read_configuration(cmd_line_args.config_file)
    archive_info_list = []
    console = Console()
    with console.status("[bold][blue]Archiving target...[/blue][bold]"):
        for target in configuration.targets:
            archiver = Archiver(target, configuration.temp_dir)
            archive_info = archiver.create_archive()
            archive_info_list.append(archive_info)
            console.print(f"Target [green][bold]{target.description}[/green][/bold] archived")
        console.print("[bold][green]All targets archived.[/bold][/green]")
    print_summary(archive_info_list, console)


if __name__ == "__main__":
    main()
