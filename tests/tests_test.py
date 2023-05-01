from eigen.tests import run
from eigen.tests import run_suite
from eigen.tests import time_suite
from eigen.tests import from_hmdna_zip

import random

def randint():
    return random.randint(-9999999, 9999999)

key = randint()
yek = 10000000

def constant():
    return key

def test_zero_args():
    assert run(constant, [key]) == True
    assert run(constant, [yek]) == (False, yek, key)

def add_one(x):
    return x + 1

def test_one_arg():
    x = randint()
    y = x + 1
    z = x - 1
    assert run(add_one, [x, y]) == True
    assert run(add_one, [x, z]) == (False, z, y)

def sum(x, y):
    return x + y

def test_two_args():
    x = randint()
    y = randint()
    ok = x + y
    ko = x + y + 1
    assert run(sum, [x, y, ok]) == True
    assert run(sum, [x, y, ko]) == (False, ko, ok)

def test_run_suite():
    suite = [[1, 2, 3], [12, -5, 7], [30, 0, 30]]
    assert run_suite(sum, suite) == 3 * [True]
    suite[1] = [12, 5, 7]
    expected = [True, (False, 7, 17), True]
    assert run_suite(sum, suite) == expected

def test_from_hmdna_zip():
    (name, tests) = from_hmdna_zip("tests/FooBar.zip")
    assert name == "FooBar"
    assert len(tests) == 3
    assert tests[0] == ['yohoho', 3, 'o']
    assert tests[1] == ['yohoho', 2, 'oh']
    assert tests[2] == ['and a bottle', 2, 'at']

def test_from_hmdna_bad_zip():
    '''Some HMDNA zip files have top directory named differently from zip file.'''
    (name1, tests1) = from_hmdna_zip("tests/FooBar.zip")
    (name2, tests2) = from_hmdna_zip("tests/BarBaz.zip")
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

def test_time_suite():
    suite = [[[1], [1]], [[1, 2, 3], [3, 2, 1]], [list(range(1, 1000)), list(range(999, 0, -1))]]
    res, time1 = time_suite(fut1, suite)
    assert res == True
    res, time2 = time_suite(fut2, suite)
    assert res == True
    assert time2 > 2*time1
    res, errors = time_suite(fut3, suite)
    assert res == False
    assert errors == run_suite(fut3, suite)

