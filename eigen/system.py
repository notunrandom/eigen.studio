from collections import defaultdict
from inspect import getmembers, isfunction, getfullargspec

import eigen.values

_register = defaultdict(lambda: defaultdict(set))


def solve(tables, functions):
    solved = defaultdict(set)
    unsolved = defaultdict(lambda: defaultdict(list))

    for key, table in tables.items():
        if key not in functions.keys():
            unsolved[key]
        else:
            for f in functions[key]:
                for i in eigen.values.inconsistencies(f, table):
                    unsolved[key][f].append(i)
                if key not in unsolved.keys() or f not in unsolved[key].keys():
                    solved[key].add(f)

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
    system = list(match_key(systems, module.__name__).values())[0]
    functions = dict(getmembers(module, isfunction))
    solution = defaultdict(set)
    for name, values in system.items():
        for function in match_key(functions, name).values():
            argspec = getfullargspec(function)
            arity = len(argspec.args)
            if argspec.defaults is not None:
                arity -= len(argspec.defaults)
            if arity == len(values[0]) - 1:
                solution[name].add(function)

    return (system, solution)


def norm(string):
    result = str()
    for c in string:
        if ord(c) in range(ord('a'), ord('z') + 1):
            result += c
        elif ord(c) in range(ord('A'), ord('Z') + 1):
            if len(result) > 0 and result[-1].islower():
                result += '_'
            result += c.lower()
        elif len(result) == 0:
            continue
        elif c == '_':
            result += c
        elif c in '- ':
            result += '_'
    return result.rstrip('_')


def match_key(dict_, name):
    return {k: v for k, v in dict_.items() if norm(k) == norm(name)}


def compare(system, solution):

    def add_time_f(table):
        def add_time(function):
            return (function, eigen.values.mean_time(function, table))
        return add_time

    def time_if_multi(item):
        key, functions = item
        if len(functions) > 1:
            return (key, set(map(add_time_f(system[key]), functions)))
        else:
            return (key, functions)

    return dict(map(time_if_multi, solution.items()))
