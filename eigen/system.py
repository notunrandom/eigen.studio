from collections import defaultdict

import eigen.values

_register = defaultdict(lambda: defaultdict(dict))


def inconsistencies(functions, system):
    _, tables = system
    for name, table in tables.items():
        if name not in functions.keys():
            for values in table:
                *args, result = values
                yield (name, args + [(result, None)])
        else:
            function = functions[name]
            for inc in eigen.values.inconsistencies(function, table):
                yield (name, inc)


def solution(system_name, solution_name, function_name):
    def solution_decorator(func):
        _register[system_name][solution_name][function_name] = func
        return func
    return solution_decorator


def solutions(system_name):
    return _register[system_name]
