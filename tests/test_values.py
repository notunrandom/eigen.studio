import pytest

from eigen.values import inconsistencies
from eigen.values import mean_time
from eigen.values import print_inconsistencies


def test_inconsistencies_1_arg():

    def mydouble(x):
        return 2 * x

    table = [[1, 2], [3, 6], [17, 34]]
    assert list(inconsistencies(mydouble, table)) == []
    table[2] = [17, 37]
    assert list(inconsistencies(mydouble, table)) == [[17, (37, 34)]]


def test_inconsistencies_2_args():

    def mysum(x, y):
        return x + y

    table = [[1, 2, 3], [12, -5, 7], [30, 0, 30]]
    assert list(inconsistencies(mysum, table)) == []
    table[1] = [12, -5, 0]
    assert list(inconsistencies(mysum, table)) == [[12, -5, (0, 7)]]


def test_print_inconsistencies():
    assert print_inconsistencies([]) == 'Total inconsistencies: 0.\n'
    assert print_inconsistencies([[1, 2, (3, 0)]]) == (
            'Total inconsistencies: 1.\n'
            '\n'
            'Inconsistency: 1\n'
            'Argument 1: 1\n'
            'Argument 2: 2\n'
            'Specified:  3\n'
            'Computed:   0\n'
            )
    incs = [['foo', 3, 1, ('fff', 'ooo')], ['baz', 2, 1, ('bb', 'aaa')]]
    assert print_inconsistencies(incs) == (
            'Total inconsistencies: 2.\n'
            '\n'
            'Inconsistency: 1\n'
            'Argument 1: foo\n'
            'Argument 2: 3\n'
            'Argument 3: 1\n'
            'Specified:  fff\n'
            'Computed:   ooo\n'
            '\n'
            'Inconsistency: 2\n'
            'Argument 1: baz\n'
            'Argument 2: 2\n'
            'Argument 3: 1\n'
            'Specified:  bb\n'
            'Computed:   aaa\n'
            )


def test_print_inconsistencies_gen():
    """print_inconsistencies can be passed the generator directly."""

    def myfun(x):
        return x

    table = [[1, 1], ['yo', 'yo'], ['ho', 'blah']]
    prnt = print_inconsistencies(inconsistencies(myfun, table))
#    assert 'Total inconsistencies' in prnt
    assert 'Specified:  blah' in prnt


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
