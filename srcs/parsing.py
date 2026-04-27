import sys
from typing import TypedDict, cast


class ParsingError(Exception):
    """Custom exception for configuration errors."""

    def __init__(self, message: str):
        super().__init__(message)


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


def _convert_value(key: str, value: str) -> int | tuple[int, int] | str | bool:
    """Helper to handle type conversions based on the key."""
    value = value.strip()
    try:
        if key in ("WIDTH", "HEIGHT"):
            if key == "WIDTH":
                if int(value) < 3:
                    raise ParsingError("Width cannot be smaller than 3")
                if int(value) < 9:
                    print("Width should be greater than 8 to display '42'", file=sys.stderr)
            if key == "HEIGHT":
                if int(value) < 3:
                    raise ParsingError("Height cannot be smaller than 3")
                if int(value) < 7:
                    print("Height should be greater than 6 to display '42'", file=sys.stderr)
            if key == "WIDTH" and int(value) > 420:
                raise ParsingError("Width cannot be greater than 420")
            if key == "HEIGHT" and int(value) > 420:
                raise ParsingError("Height cannot be greater than 420")
            return int(value)
        if key in ("ENTRY", "EXIT"):
            x, y = map(int, value.split(","))
            return x, y
        if key == "PERFECT":
            if value == "True":
                return True
            if value == "False":
                return False
            raise ValueError
        return value
    except ValueError:
        raise ParsingError(f"Invalid value for '{key}': '{value}'")


def _check_values(_config: MazeConfig) -> None:
    _entry: tuple[int, int] = _config["ENTRY"]
    _exit: tuple[int, int] = _config["EXIT"]

    for x, y in [_entry, _exit]:
        if x < 0 or x >= _config["WIDTH"]:
            raise ParsingError("Entry and exit must be inside the maze")
        if y < 0 or y >= _config["HEIGHT"]:
            raise ParsingError("Entry and exit must be inside the maze")

    if _entry == _exit:
        raise ParsingError(
            "Entry and exit must be different cells of the maze"
        )


class Parser:
    """Parses maze configuration parameters from
    the file passed as sys.argv[1]."""

    parameters = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED",
    }

    def __init__(self) -> None:
        self.config: MazeConfig = self._parse_txt()

    def _parse_txt(self) -> MazeConfig:
        """Reads the file and populates the config dictionary."""
        raw: dict[str, int | tuple[int, int] | str | bool] = {}

        try:
            with open(sys.argv[1], "r") as f:
                for line in f:
                    if line[0] == "#":
                        continue
                    try:
                        key, value = line.strip().split("=")
                    except Exception:
                        raise ParsingError(f"Invalid or empty line: {line}")
                    if key not in self.parameters or not value:
                        raise ParsingError(
                            f"Invalid argument in '{sys.argv[1]}': "
                            f"'{key}={value}'"
                        )
                    raw[key] = _convert_value(key, value)

            missing = self.parameters - raw.keys()
            if missing:
                raise ParsingError(f"Missing required parameters: "
                                   f"{str(missing).strip('{}')}")

            _config = cast(MazeConfig, cast(object, raw))
            _check_values(_config)
            return _config

        except FileNotFoundError:
            raise Exception(f"[ERROR] File not found: {sys.argv[1]}")
        except ParsingError as _e:
            raise Exception(f"[PARSING ERROR] {_e}")
        except Exception as _e:
            raise Exception(f"[ERROR] Unexpected error: {_e}")


if __name__ == "__main__":
    try:
        config = Parser().config
        print(config)
    except Exception as e:
        print(e)
