#
# Copyright 2023 Jaroslav Chmurny
#
# This file is part of Rudimentary Backup.
#
# Rudimentary Backup is free software. It is licensed under the Apache
# License, Version 2.0 # (the "License"); you may not use this file except
# in compliance with the # License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from dataclasses import dataclass
from os.path import isdir
from re import match

from yaml import safe_load


@dataclass(frozen=True)
class Target:
    description: str
    source_path: str
    archive_name: str
    include_patterns: tuple[str, ...] | None
    exclude_patterns: tuple[str, ...] | None

    def _has_include_patterns(self) -> bool:
        if self.include_patterns is None:
            return False
        return len(self.include_patterns) > 0

    def _is_included(self, filename: str) -> bool:
        for pattern in self.include_patterns:
            if match(pattern, filename):
                return True
        return False

    def _has_exclude_patterns(self) -> bool:
        if self.exclude_patterns is None:
            return False
        return len(self.exclude_patterns) > 0

    def _is_excluded(self, filename: str) -> bool:
        for pattern in self.exclude_patterns:
            if match(pattern, filename):
                return True
        return False

    def is_relevant(self, filename: str) -> bool:
        if self.include_patterns is None and self.exclude_patterns is None:
            return True

        if self._has_include_patterns():
            return self._is_included(filename)
        
        if self._has_exclude_patterns():
            return not self._is_excluded(filename)

        message = "Single target cannot have both include and exclude patterns."
        raise InvalidConfigurationError(message)


@dataclass(frozen=True)
class Configuration:
    temp_dir: str
    destination_dir: str
    targets: tuple[Target, ...]


class InvalidConfigurationError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def _read_single_target(yaml_data: dict[str, str]) -> Target:
    DESCRIPTION = "description"
    SOURCE_PATH = "source-path"
    ARCHIVE_NAME = "archive-name"
    INCLUDE_PATTERNS = "include-patterns"
    EXCLUDE_PATTERNS = "exclude-patterns"

    if SOURCE_PATH not in yaml_data:
        message = f"Missing '{SOURCE_PATH}' element in one of the targets."
        raise InvalidConfigurationError(message)
    source_path = yaml_data[SOURCE_PATH]
    if not isdir(source_path):
        message = f"Source path '{source_path}' is not a directory."
        raise InvalidConfigurationError(message)
    
    if ARCHIVE_NAME not in yaml_data:
        message = f"Missing '{ARCHIVE_NAME}' element in one of the targets."
        raise InvalidConfigurationError(message)

    include_patterns = None
    exclude_patterns = None
    if INCLUDE_PATTERNS in yaml_data:
        include_patterns = yaml_data[INCLUDE_PATTERNS]
    if EXCLUDE_PATTERNS in yaml_data:
        exclude_patterns = yaml_data[EXCLUDE_PATTERNS]

    return Target(
        description=yaml_data[DESCRIPTION],
        source_path=yaml_data[SOURCE_PATH],
        archive_name=yaml_data[ARCHIVE_NAME],
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns
    )


def _read_targets(yaml_data: list[dict[str, str]]) -> tuple[Target, ...]:
    result = []
    for target in yaml_data:
        result.append(_read_single_target(target))
    return tuple(result)


def read_configuration(filename: str) -> Configuration:
    TEMP_DIR = "temp-dir"
    DESTINATION_DIR = "destination-dir"
    TARGETS = "targets"

    with open(filename, "r") as config_file:
        yaml_data = safe_load(config_file)
        if TEMP_DIR not in yaml_data:
            message = f"'{TEMP_DIR}' element missing in the configuration file '{filename}'."
            raise InvalidConfigurationError(message)
        if DESTINATION_DIR not in yaml_data:
            message = f"'{DESTINATION_DIR}' element missing in the configuration file '{filename}'."
            raise InvalidConfigurationError(message)
        if "targets" not in yaml_data:
            message = f"'{TARGETS}' element missing in the configuration file '{filename}'."
            raise InvalidConfigurationError(message)
        return Configuration(
            temp_dir=yaml_data[TEMP_DIR],
            destination_dir=yaml_data[DESTINATION_DIR],
            targets=_read_targets(yaml_data["targets"])
        )
