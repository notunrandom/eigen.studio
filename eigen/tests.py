from enum import Enum
from functools import partial
from pathlib import PurePath
from zipfile import ZipFile
from zipfile import Path

Result = Enum('Result', ['PASS', 'FAIL'])

def from_hmdna_zip(path):
    path = PurePath(path)
    tests = []
    with ZipFile(path) as zfile:
        contents = zfile.namelist()
        prefix = path.stem + "/inputs/input_"
        files = [f for f in contents if f.startswith(prefix)]
        files.sort()
        for f in files:
            test = []
            with zfile.open(f) as file:
                for line in file:
                    test.append(line)
            f = f.replace("input", "output")
            with zfile.open(f) as file:
                for line in file:
                    test.append(line)
            test = [t.decode('UTF-8').strip() for t in test]
            tests.append(_convert(test))
    return (path.stem, tests)

def _convert(data):
    for i in range(len(data)):
        if data[i].isdigit():
            data[i] = int(data[i])
    return data

def run(function, data):
    f = function
    *args, expected = data
    for arg in args:
        f = partial(f, arg)
    result = f()
    if result == expected:
        return Result.PASS
    else:
        return (Result.FAIL, expected, result)

def run_suite(function, suite):
    return [run(function, data) for data in suite]
