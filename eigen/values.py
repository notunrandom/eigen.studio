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


def print_inconsistencies(incs):
    """Pretty-print result of inconsistencies()."""

    ndif = len(incs)
    result = f'Total inconsistencies: {ndif}.\n'
    for i in range(ndif):
        result += f'\nInconsistency: {i+1}\n'
        inc = incs[i]
        narg = len(inc) - 1
        for j in range(narg):
            result += f'Argument {j+1}: {inc[j]}\n'
        spec, comp = inc[-1]
        result += f'Specified:  {spec}\n'
        result += f'Computed:   {comp}\n'
    return result


def mean_time(function, table):
    """If function is correct, compute mean execution time."""

    def ensure_no_differences():
        assert differences(function, table) == []
    n, s = timeit.Timer(ensure_no_differences).autorange()
    return s/n
