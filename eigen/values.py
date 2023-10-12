from functools import partial
from functools import reduce
from pathlib import PurePath
from zipfile import ZipFile
import timeit


def apply_function(function: callable, values: list) -> list:
    """Apply the given function to the input values.

    function: a callable taking n-1 arguments.
    values: a list with n-1 input values and one expected output value.
    returns: the same input values followed by the actual output value.
    """
    f = function
    *args, value = values
    for arg in args:
        f = partial(f, arg)
    return args + [f()]


def differences(function: callable, table: list) -> list:
    """Differences between the truth table and the image.

    function: a callable taking n-1 arguments.
    table: a truth table, i.e. each row is a list of values (n-1 inputs
    followed by the expected result.
    returns: the differences between the truth table and the actual
    image of applying the function.
    """

    image = [apply_function(function, values) for values in table]
    return [values for values in image if values not in table]


def print_differences(differences, values):
    """Pretty-print differences between a truth table and image."""

    ndif = len(differences)
    nval = len(values)
    result = f'{ndif} difference(s) given {nval} value(s).\n'
    for i in range(ndif):
        result += f'\nDifference: {i+1}\n'
        diff = differences[i]
        narg = len(diff) - 1
        for j in range(narg):
            result += f'Argument {j+1}: {diff[j]}\n'
        for j in range(i, nval):
            value = values[j]
            if value[:-1] == diff[:-1]:
                break
        result += f'Specified:  {value[-1]}\n'
        result += f'Computed:   {diff[-1]}\n'
    return result


def mean_time(function, table):
    """If function is correct, compute mean execution time."""

    def ensure_no_differences():
        assert differences(function, table) == []
    n, s = timeit.Timer(ensure_no_differences).autorange()
    return s/n


def value_table_from_HMDNA_zip(path):
    """Read test files .zip provided with exercises in the 'Hidden
    messages in DNA' course in bioinformatics (on Coursera).
    """

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
            test = [t.decode('UTF-8').strip().split() for t in test]
            tests.append([_convert(t) for t in test])
    return (path.stem, _normalise(tests))


def _convert(data):
    for i in range(len(data)):
        if data[i].isdigit():
            data[i] = int(data[i])
    return data


def _normalise(lists):

    def max_lengths(lengths, lists):
        return [max(acc, len(item)) for acc, item in zip(lengths, lists)]

    lengths = reduce(max_lengths, lists, [0 for _ in lists[0]])
    norm = []
    for item in lists:
        n = []
        for item, length in zip(item, lengths):
            n.append(item if length > 1 else item[0])
        norm.append(n)
    return norm
