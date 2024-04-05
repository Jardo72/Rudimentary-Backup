from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import datetime

from colorama import init as init_colorama

from archiver import Archiver
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

    # optional arguments
    parser.add_argument(
        "-c", "--no-color",
        dest="no_color",
        default=False,
        action="store_true",
        help="if specified, the output will not use any colors"
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    init_colorama()
    cmd_line_args = parse_cmd_line_args()
    configuration = read_configuration(cmd_line_args.config_file)
    start_time = current_timestamp()
    archive_info_list = []
    for target in configuration.targets:
        archiver = Archiver(target, configuration.temp_dir)
        archive_info = archiver.create_archive()
        print(archive_info)
        archive_info_list.append(archive_info)
    end_time = current_timestamp()

    print()
    print(f"Start time: {start_time}")
    print(f"End time:   {end_time}")


if __name__ == "__main__":
    main()
