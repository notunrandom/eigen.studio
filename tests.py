from enum import Enum
from functools import partial

Result = Enum('Result', ['PASS', 'FAIL'])

def run(function, args, expected):
    f = function
    for arg in args:
        f = partial(f, arg)
    result = f()
    if result == expected:
        return Result.PASS
    else:
        return (Result.FAIL, expected, result)