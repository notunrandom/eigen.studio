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


def print_inconsistencies(incs):
    """Pretty-print result of inconsistencies()."""

    result = ''
    i = 0
    for inc in incs:
        result += f'\nInconsistency: {i+1}\n'
        narg = len(inc) - 1
        for j in range(narg):
            result += f'Argument {j+1}: {inc[j]}\n'
        spec, comp = inc[-1]
        result += f'Specified:  {spec}\n'
        result += f'Computed:   {comp}\n'
        i += 1

    return f'Total inconsistencies: {i}.\n' + result


def mean_time(function, table):
    """If function is correct, compute mean execution time."""

    def ensure_no_inconsistencies():
        assert list(inconsistencies(function, table)) == []
    n, s = timeit.Timer(ensure_no_inconsistencies).autorange()
    return s/n
