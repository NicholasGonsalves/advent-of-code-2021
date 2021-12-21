# Common AoC code
# e.g. reading and parsing inputs
from typing import List


def read_file(file_name: str, delimiter: str = "\n") -> List[str]:
    with open(file_name) as f:
        inputs = f.read()

    return [i for i in inputs.split(delimiter)]
