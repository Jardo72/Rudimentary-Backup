from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from datetime import datetime
from os import walk
from os.path import getsize, join, relpath
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED

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
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    configuration = read_configuration(cmd_line_args.config_file)
    print(configuration)
    return

    root = argv[1]
    print(current_timestamp())
    archive_name = f"test-{current_timestamp()}.zip"
    with ZipFile(archive_name, "w", ZIP_DEFLATED) as archive:
        for dir, _, files in walk(root, topdown=True):
            for file in files:
                pathname = join(dir, file)
                entry = relpath(pathname, join(root, ".."))
                archive.write(pathname, entry)
                getsize(pathname)
                # TODO: remove
                # print()
                # print(60 * "=")
                # print(f"Path = {pathname}")
                # print(f"Entry = {entry}")


if __name__ == "__main__":
    main()
