from tests import run
from tests import Result

import random

def randint():
    return random.randint(-9999999, 9999999)

key = randint()
yek = 10000000

def constant():
    return key

def test_zero_args():
    assert run(constant, [key]) == Result.PASS
    assert run(constant, [yek]) == (Result.FAIL, yek, key)

def add_one(x):
    return x + 1

def test_one_arg():
    x = randint()
    y = x + 1
    z = x - 1
    assert run(add_one, [x, y]) == Result.PASS
    assert run(add_one, [x, z]) == (Result.FAIL, z, y)

def sum(x, y):
    return x + y

def test_two_args():
    x = randint()
    y = randint()
    ok = x + y
    ko = x + y + 1
    assert run(sum, [x, y, ok]) == Result.PASS
    assert run(sum, [x, y, ko]) == (Result.FAIL, ko, ok)

