from collections import defaultdict
from inspect import getmembers, isfunction

import eigen.values

_register = defaultdict(lambda: defaultdict(set))


def solve(tables, functions):
    solved = defaultdict(set)
    unsolved = defaultdict(lambda: defaultdict(list))

    for name, table in tables.items():
        if name not in functions.keys():
            for values in table:
                *args, result = values
                unsolved[name]
        else:
            for f in functions[name]:
                for i in eigen.values.inconsistencies(f, table):
                    unsolved[name][f].append(i)
            if name not in unsolved.keys() or f not in unsolved[name].keys():
                solved[name].add(f)

    return (solved, unsolved)


def matchfun(func):
    return (func.__module__, func.__name__)


def solution(func):
    _register[func.__module__][func.__name__].add(func)
    return func


def solves(system, function):
    def decorator(func):
        _register[system][function].add(func)
        return func
    return decorator


def solutions(sys):
    return _register[sys]


def match(systems, module):
    system = systems[module.__name__]
    solution = defaultdict(set)
    for name, _ in system.items():
        solution[name] = {dict(getmembers(module, isfunction))[name]}

    return (module.__name__, system, solution)
