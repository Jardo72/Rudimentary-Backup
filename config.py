from dataclasses import dataclass
from os.path import isdir
from re import match

from yaml import safe_load


@dataclass(frozen=True)
class Target:
    description: str
    source_path: str
    destination_path: str
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

        # TODO:
        # raise an exception - this should never be reached


@dataclass(frozen=True)
class Configuration:
    temp_dir: str
    targets: tuple[Target, ...]


class InvalidConfigurationError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def _read_single_target(yaml_data: dict[str, str]) -> Target:
    DESCRIPTION = "description"
    SOURCE_PATH = "source-path"
    DESTINATION_PATH = "destination-path"
    INCLUDE_PATTERNS = "include-patterns"
    EXCLUDE_PATTERNS = "exclude-patterns"

    if SOURCE_PATH not in yaml_data:
        message = f"Missing '{SOURCE_PATH}' element in one of the targets."
        raise InvalidConfigurationError(message)
    source_path = yaml_data[SOURCE_PATH]
    if not isdir(source_path):
        message = f"Source path '{source_path}' is not a directory."
        raise InvalidConfigurationError(message)
    
    if DESTINATION_PATH not in yaml_data:
        message = f"Missing '{DESTINATION_PATH}' element in one of the targets."
        raise InvalidConfigurationError(message)
    destination_path = yaml_data[DESTINATION_PATH]
    if not isdir(destination_path):
        message = f"Destination path '{destination_path}' is not a directory."
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
        destination_path=yaml_data[DESTINATION_PATH],
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
    TARGETS = "targets"

    with open(filename, "r") as config_file:
        yaml_data = safe_load(config_file)
        if TEMP_DIR not in yaml_data:
            message = f"'{TEMP_DIR}' element missing in the configuration file '{filename}'."
            raise InvalidConfigurationError(message)
        if "targets" not in yaml_data:
            message = f"'{TARGETS}' element missing in the configuration file '{filename}'."
            raise InvalidConfigurationError(message)
        return Configuration(
            temp_dir=yaml_data[TEMP_DIR],
            targets=_read_targets(yaml_data["targets"])
        )
