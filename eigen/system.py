from collections import defaultdict

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


def solution(match=matchfun):
    def solution_decorator(func):
        (sys, fname) = match(func)
        _register[sys][fname].add(func)
        return func
    return solution_decorator


def solutions(sys):
    return _register[sys]
