import random
import pytest

from eigen.values import apply_function
from eigen.values import differences
from eigen.values import mean_time
from eigen.values import print_differences


def _randint():
    return random.randint(-9999999, 9999999)


def test_apply_zero_args():
    """Show that apply_function can be passed a 0-argument function.
    It must also be passed a list with an (unused) expected value.
    It returns a single-element list which contains the return value.
    """

    KEY = _randint()
    YEK = 10000000

    def constant():
        return KEY

    assert apply_function(constant, [KEY]) == [KEY]
    assert apply_function(constant, [YEK]) == [KEY]


def test_apply_one_arg():
    """Show that apply_function can be passed a 1-argument function.
    It must also be passed a list with the argument and an (unused)
    expected value. It returns a list with the argument and the
    returned value.
    """

    def add_one(x):
        return x + 1

    x = _randint()
    y = x + 1
    z = x - 1

    assert apply_function(add_one, [x, y]) == [x, y]
    assert apply_function(add_one, [x, z]) == [x, y]


def _mysum(x, y):
    return x + y


def test_apply_two_args():
    """Show that apply_function can be passed a 2-argument function.
    It must also be passed a list with the arguments and an (unused)
    expected value. It returns a list with the arguments and the
    returned value.
    """

    x = _randint()
    y = _randint()
    ok = x + y
    ko = x + y + 1
    assert apply_function(_mysum, [x, y, ok]) == [x, y, ok]
    assert apply_function(_mysum, [x, y, ko]) == [x, y, ok]


def test_differences():
    table = [[1, 2, 3], [12, -5, 7], [30, 0, 30]]
    assert differences(_mysum, table) == []
    table[1] = [12, -5, 0]
    assert differences(_mysum, table) == [[12, -5, 7]]


def test_print_differences():
    assert print_differences([], [[1, 2, 3]]) \
        == '0 difference(s) given 1 value(s).\n'
    assert print_differences([], [[1, 2, 3], [2, 3, 5]]) \
        == '0 difference(s) given 2 value(s).\n'
    assert print_differences([[1, 2, 0]], [[1, 2, 3]]) == (
            '1 difference(s) given 1 value(s).\n'
            '\n'
            'Difference: 1\n'
            'Argument 1: 1\n'
            'Argument 2: 2\n'
            'Specified:  3\n'
            'Computed:   0\n'
            )
    difs = [['foo', 3, 1, 'ooo'], ['baz', 2, 1, 'aaa']]
    vals = [['foo', 3, 1, 'fff'], ['bar', 1, 1, 'b'], ['baz', 2, 1, 'bb']]
    assert print_differences(difs, vals) == (
            '2 difference(s) given 3 value(s).\n'
            '\n'
            'Difference: 1\n'
            'Argument 1: foo\n'
            'Argument 2: 3\n'
            'Argument 3: 1\n'
            'Specified:  fff\n'
            'Computed:   ooo\n'
            '\n'
            'Difference: 2\n'
            'Argument 1: baz\n'
            'Argument 2: 2\n'
            'Argument 3: 1\n'
            'Specified:  bb\n'
            'Computed:   aaa\n'
            )


def test_mean_time():
    """Show that mean_time is different for a correct and inefficient
    implementation, but raises an exception for an incorrect one.
    """

    def fut1(xs):
        """Normal implementation of list reversal."""
        return list(reversed(xs))

    def fut2(xs):
        """Really inefficient implementation of list reversal."""
        rev = list(reversed(xs))
        inc = [x + 1 for x in rev]
        inc.reverse()
        dec = [x - 1 for x in inc]
        return list(reversed(dec))

    def fut3(xs):
        """Incorrect implementation of list reversal."""
        return xs

    table = [
        [[1], [1]],
        [[1, 2, 3], [3, 2, 1]],
        [list(range(1, 1000)), list(range(999, 0, -1))]]

    time1 = mean_time(fut1, table)
    time2 = mean_time(fut2, table)
    assert time2 > 2*time1
    with pytest.raises(Exception):
        _ = mean_time(fut3, table)
