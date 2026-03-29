import sys


class Parser:
    parameters: set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }

    def __init__(self):
        self.config: dict[str, str] = dict()
        self.parse_txt()

    def parse_txt(self) -> None:
        try:
            with open(sys.argv[1]) as config:
                for line in config:
                    param, value = line.split('=')
                    value = value.strip()
                    if param not in self.parameters or not value:
                        raise Exception(
                            f"[ERROR] Invalid argument in '{sys.argv[1]}': "
                            f"'{param}={value}'")
                    self.config[param] = value
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    print(Parser().config)
