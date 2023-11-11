from collections import defaultdict
from inspect import getmembers, isfunction, getfullargspec

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
    for name, values in system.items():
        functions = dict(getmembers(module, isfunction))
        if name in functions.keys():
            function = functions[name]
            arity = len(getfullargspec(function).args)
            if arity == len(values[0]) - 1:
                solution[name] = {dict(getmembers(module, isfunction))[name]}

    return (module.__name__, system, solution)


def name(string):
    result = str()
    for c in string:
        if ord(c) in range(ord('a'), ord('z') + 1):
            result += c
        if ord(c) in range(ord('A'), ord('Z') + 1):
            if len(result) > 0 and result[-1].islower():
                result += '_'
            result += c.lower()
        elif c == '_':
            result += c
        elif c in '- ':
            result += '_'
    return result
