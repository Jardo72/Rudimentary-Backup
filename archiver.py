from dataclasses import dataclass
from enum import Enum, unique
from os import walk
from os.path import getsize, join, relpath, split
from shutil import move
from zipfile import ZipFile, ZIP_DEFLATED

from config import Target


@unique
class ArchiveStatus(Enum):
    OK = "OK"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ArchiveInfo:
    target: Target
    archived_file_count: int
    archived_byte_count: int
    ignored_file_count: int
    archive_size: int
    status: ArchiveStatus


class Archiver:

    def __init__(self, target: Target, temp_dir: str, destination_dir: str) -> None:
        self._target = target
        self._temp_dir = temp_dir
        self._destination_dir = destination_dir

    def create_archive(self) -> ArchiveInfo:
        archive_name = join(self._temp_dir, f"{self._target.archive_name}.zip")
        archived_file_count = 0
        archived_byte_count = 0
        ignored_file_count = 0
        with ZipFile(archive_name, "w", ZIP_DEFLATED) as archive:
            for dir, _, files in walk(self._target.source_path, topdown=True):
                for file in files:
                    pathname = join(dir, file)
                    if self._target.is_relevant(pathname):
                        entry = relpath(pathname, join(self._target.source_path, ".."))
                        archive.write(pathname, entry)
                        archived_byte_count += getsize(pathname)
                        archived_file_count += 1
                    else:
                        ignored_file_count += 1
        archive_size = getsize(archive_name)
        move(archive_name, self._destination_dir)
        return ArchiveInfo(
            target=self._target,
            archived_file_count=archived_file_count,
            archived_byte_count=archived_byte_count,
            ignored_file_count=ignored_file_count,
            archive_size=archive_size,
            status=ArchiveStatus.OK,
        )
