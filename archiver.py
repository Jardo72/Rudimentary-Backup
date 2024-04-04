from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto, unique
from os import walk
from os.path import getsize, join, relpath, split
from zipfile import ZipFile, ZIP_DEFLATED

from config import Target


def _current_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


@unique
class ArchiveStatus(Enum):
    OK = auto()
    FAILED = auto()


@dataclass(frozen=True)
class ArchiveInfo:
    target: Target
    file_count: int
    byte_count: int
    archive_size: int
    status: ArchiveStatus


class Archiver:

    def __init__(self, target: Target, temp_dir: str) -> None:
        self._target = target
        self._temp_dir = temp_dir

    def create_archive(self) -> ArchiveInfo:
        _, source_dir = split(self._target.source_path)
        archive_name = join(self._temp_dir, f"{source_dir}-{_current_timestamp()}.zip")
        file_count = 0
        byte_count = 0
        with ZipFile(archive_name, "w", ZIP_DEFLATED) as archive:
            for dir, _, files in walk(self._target.source_path, topdown=True):
                for file in files:
                    pathname = join(dir, file)
                    entry = relpath(pathname, join(self._target.source_path, ".."))
                    archive.write(pathname, entry)
                    byte_count += getsize(pathname)
                    file_count += 1
            return ArchiveInfo(
                target=self._target,
                file_count=file_count,
                byte_count=byte_count,
                archive_size=getsize(archive_name),
                status=ArchiveStatus.OK,
            )
