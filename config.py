from dataclasses import dataclass

from yaml import safe_load


@dataclass(frozen=True)
class Target:
    description: str
    source_path: str
    destination_path: str
    include_patterns: tuple[str, ...] | None
    exclude_patterns: tuple[str, ...] | None


@dataclass(frozen=True)
class Configuration:
    temp_dir: str
    targets: tuple[Target, ...]


def _read_single_target(yaml_data: dict[str, str]) -> Target:
    return Target(
        description=yaml_data["description"],
        source_path=yaml_data["source-path"],
        destination_path=yaml_data["destination-path"],
        include_patterns=None,
        exclude_patterns=None
    )


def _read_targets(yaml_data: list[dict[str, str]]) -> tuple[Target, ...]:
    result = []
    for target in yaml_data:
        result.append(_read_single_target(target))
    return tuple(result)


def read_configuration(filename: str) -> Configuration:
    with open(filename, "r") as config_file:
        yaml_data = safe_load(config_file)
        if "temp-dir" not in yaml_data:
            # TODO: raise an exception
            ...
        if "targets" not in yaml_data:
            # TODO: raise an exception
            ...
        return Configuration(
            temp_dir=yaml_data["temp-dir"],
            targets=_read_targets(yaml_data["targets"])
        )
