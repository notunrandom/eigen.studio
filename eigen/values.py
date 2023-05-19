from functools import partial
from pathlib import PurePath
from zipfile import ZipFile
import timeit


def apply_function(function, values):
    f = function
    *args, value = values
    for arg in args:
        f = partial(f, arg)
    return args + [f()]


def differences(function, table):
    image = [apply_function(function, values) for values in table]
    return [values for values in image if values not in table]


def mean_time(function, table):
    def ensure_no_differences():
        assert differences(function, table) == []
    n, s = timeit.Timer(ensure_no_differences).autorange()
    return s/n


def value_table_from_HMDNA_zip(path):
    path = PurePath(path)
    tests = []
    with ZipFile(path) as zfile:
        contents = zfile.namelist()
        files = [f for f in contents if '/inputs/input_' in f]
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
