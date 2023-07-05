from functools import partial
from pathlib import PurePath
from zipfile import ZipFile
import timeit
from enum import IntEnum


def apply_function(function, values):
    f = function
    *args, value = values
    for arg in args:
        f = partial(f, arg)
    return args + [f()]


def differences(function, table):
    image = [apply_function(function, values) for values in table]
    return [values for values in image if values not in table]


def print_differences(differences, values):
    ndif = len(differences)
    nval = len(values)
    result = f'{ndif} difference(s) given {nval} value(s).\n'
    for i in range(ndif):
        result += f'\nDifference: {i+1}\n'
        diff = differences[i]
        narg = len(diff) - 1
        for j in range(narg):
            result += f'Argument {j+1}: {diff[j]}\n'
        for j in range(i, nval):
            value = values[j]
            if value[:-1] == diff[:-1]:
                break
        result += f'Specified:  {value[-1]}\n'
        result += f'Computed:   {diff[-1]}\n'
    return result


def mean_time(function, table):
    def ensure_no_differences():
        assert differences(function, table) == []
    n, s = timeit.Timer(ensure_no_differences).autorange()
    return s/n


def value_table_from_HMDNA_zip(path):
    path = PurePath(path)
    tests = []
    with ZipFile(path) as zfile:
        contents = zfile.namelist()
        files = [f for f in contents if '/inputs/input_' in f]
        files.sort()
        for f in files:
            test = []
            with zfile.open(f) as file:
                for line in file:
                    test.append(line)
            f = f.replace("input", "output")
            with zfile.open(f) as file:
                for line in file:
                    test.append(line)
            test = [t.decode('UTF-8').strip() for t in test]
            tests.append(_convert(test))
    return (path.stem, tests)


def _convert(data):
    for i in range(len(data)):
        if data[i].isdigit():
            data[i] = int(data[i])
    return data


def infer(string):
    parse = _parser(_tokens(string))
    return parse(string)


_Token = IntEnum('_Token', ['ALPHA', 'DIGIT', 'DOT', 'SPACE'])


def _tokens(string):
    seen = set()
    tokens = list()
    for c in string:
        if c.isdigit():
            _append_if_first(seen, tokens, _Token.DIGIT)
        elif c == '.':
            _append_if_first(seen, tokens, _Token.DOT)
        elif c.isalpha():
            _append_if_first(seen, tokens, _Token.ALPHA)
        elif c.isspace():
            _append_if_first(seen, tokens, _Token.SPACE)
    return sorted(tokens)


def _append_if_first(seen, tokens, token):
    if token not in seen:
        seen.add(token)
        tokens.append(token)


def _parser(tokens):
    print(tokens)
    match tokens:
        case [_Token.ALPHA, *_]:
            return lambda string: string
        case [_Token.DIGIT]:
            return lambda string: int(string)
        case [_Token.DIGIT, _Token.DOT]:
            return lambda string: float(string)
        case [_Token.DIGIT, _Token.SPACE] | \
                [_Token.DIGIT, _Token.DOT, _Token.SPACE]:
            return lambda string: [infer(s) for s in string.split()]
