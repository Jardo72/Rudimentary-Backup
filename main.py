from datetime import datetime
from os import walk
from os.path import join, relpath
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED


def current_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main() -> None:
    root = argv[1]
    print(current_timestamp())
    archive_name = f"test-{current_timestamp()}.zip"
    with ZipFile(archive_name, "w", ZIP_DEFLATED) as archive:
        for dir, _, files in walk(root, topdown=True):
            for file in files:
                pathname = join(dir, file)
                entry = relpath(pathname, join(root, ".."))
                archive.write(pathname, entry)
                # print()
                # print(60 * "=")
                # print(f"Path = {pathname}")
                # print(f"Entry = {entry}")


if __name__ == "__main__":
    main()
