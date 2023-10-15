from functools import partial
import timeit


def inconsistencies(function, table):
    for *args, expected in table:
        f = function
        for arg in args:
            f = partial(f, arg)
        image = f()
        if image != expected:
            yield args + [(expected, image)]


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
