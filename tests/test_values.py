import random
import pytest

from eigen.values import apply_function
from eigen.values import differences
from eigen.values import mean_time
from eigen.values import value_table_from_HMDNA_zip


def randint():
    return random.randint(-9999999, 9999999)


key = randint()
yek = 10000000


def constant():
    return key


def test_apply_zero_args():
    assert apply_function(constant, [key]) == [key]
    assert apply_function(constant, [yek]) == [key]


def add_one(x):
    return x + 1


def test_apply_one_arg():
    x = randint()
    y = x + 1
    z = x - 1
    assert apply_function(add_one, [x, y]) == [x, y]
    assert apply_function(add_one, [x, z]) == [x, y]


def mysum(x, y):
    return x + y


def test_apply_two_args():
    x = randint()
    y = randint()
    ok = x + y
    ko = x + y + 1
    assert apply_function(mysum, [x, y, ok]) == [x, y, ok]
    assert apply_function(mysum, [x, y, ko]) == [x, y, ok]


def test_differences():
    table = [[1, 2, 3], [12, -5, 7], [30, 0, 30]]
    assert differences(mysum, table) == []
    table[1] = [12, -5, 0]
    assert differences(mysum, table) == [[12, -5, 7]]


def test_HMDNA_zip():
    (name, tests) = value_table_from_HMDNA_zip("tests/FooBar.zip")
    assert name == "FooBar"
    assert len(tests) == 3
    assert tests[0] == ['yohoho', 3, 'o']
    assert tests[1] == ['yohoho', 2, 'oh']
    assert tests[2] == ['and a bottle', 2, 'at']


def test_HMDNA_bad_zip():
    """Some HMDNA zip files have top directory named
    differently from zip file.
    """
    (name1, tests1) = value_table_from_HMDNA_zip("tests/FooBar.zip")
    (name2, tests2) = value_table_from_HMDNA_zip("tests/BarBaz.zip")
    assert name1 == 'FooBar'
    assert name2 == 'BarBaz'
    assert tests2 == tests1


def fut1(xs):
    return list(reversed(xs))


def fut2(xs):
    rev = list(reversed(xs))
    inc = [x + 1 for x in rev]
    inc.reverse()
    dec = [x - 1 for x in inc]
    return list(reversed(dec))


def fut3(xs):
    return xs


def test_mean_time():
    table = [
        [[1], [1]],
        [[1, 2, 3], [3, 2, 1]],
        [list(range(1, 1000)), list(range(999, 0, -1))]]
    time1 = mean_time(fut1, table)
    time2 = mean_time(fut2, table)
    assert time2 > 2*time1
    with pytest.raises(Exception):
        _ = mean_time(fut3, table)
