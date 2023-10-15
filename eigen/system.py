import eigen.values


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
