import sys


class ParsingError(Exception):
    """Custom exception for configuration errors."""
    def __init__(self, message: str):
        super().__init__(message)


def _convert_value(key: str, value: str) -> int | tuple[int, int] | str | bool:
    """Helper to handle type conversions based on the key."""
    value = value.strip()
    try:
        if key in ("WIDTH", "HEIGHT"):
            return int(value)
        if key in ("ENTRY", "EXIT"):
            x, y = map(int, value.split(','))
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


class Parser:
    """Parses maze configuration parameters from
    the file passed as sys.argv[1]."""
    parameters = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }

    def __init__(self) -> None:
        self.config: dict[str, int | tuple[int, int] | str | bool] = {}
        try:
            self.parse_txt()
        except Exception as e:
            raise Exception(e)

    def parse_txt(self) -> None:
        """Reads the file and populates the config dictionary."""
        try:
            with open(sys.argv[1], "r") as f:
                for line in f:
                    if line[0] == '#':
                        continue
                    key, value = line.strip().split('=')
                    if key not in self.parameters or not value:
                        raise ParsingError(f"Invalid argument in "
                                           f"'{sys.argv[1]}': '{key}={value}'")
                    self.config[key] = _convert_value(key, value)

        except FileNotFoundError:
            raise Exception(f"[ERROR] File not found: {sys.argv[1]}")
        except ParsingError as e:
            raise Exception(f"[PARSING ERROR] {e}")
        except Exception as e:
            raise Exception(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    parser = Parser()
    print(parser.config)
