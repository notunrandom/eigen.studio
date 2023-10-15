from functools import reduce
from pathlib import PurePath, Path
from zipfile import ZipFile


def system(pathstr):
    """Read all tests from all .zip files in a directory of .zip files
    provided with exercises in the 'Hidden messages in DNA' course in
    bioinformatics (on Coursera)."""

    path = Path(pathstr)
    sysname = path.stem
    tables = dict()
    for p in Path(path).glob('**/*.zip'):
        name, table = unzip(p)
        tables[name] = table
    return (sysname, tables)


def unzip(path):
    """Read test files from .zip provided with exercises in the 'Hidden
    messages in DNA' course in bioinformatics (on Coursera).
    """

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
            test = [t.decode('UTF-8').strip().split() for t in test]
            tests.append([_convert(t) for t in test])
    return (path.stem, _normalise(tests))


def _convert(data):
    for i in range(len(data)):
        if data[i].isdigit():
            data[i] = int(data[i])
    return data


def _normalise(lists):

    def max_lengths(lengths, lists):
        return [max(acc, len(item)) for acc, item in zip(lengths, lists)]

    lengths = reduce(max_lengths, lists, [0 for _ in lists[0]])
    norm = []
    for item in lists:
        n = []
        for item, length in zip(item, lengths):
            n.append(item if length > 1 else item[0])
        norm.append(n)
    return norm
