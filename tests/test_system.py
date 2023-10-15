from eigen.system import inconsistencies


def test_inconsistencies_empty_system():

    system = ('empty', dict())
    assert list(inconsistencies({}, system)) == []


def test_inconsistencies_none():
    addition = ('add', [[13, 17, 30]])
    system = ('arithmetic', dict([addition]))

    def myadd(x, y):
        return x + y

    solution = {'add': myadd}
    assert list(inconsistencies(solution, system)) == []


def test_inconsistencies():
    addition = ('add', [[5, 1, 6], [13, 17, 30]])
    subtraction = ('subtract', [[5, 1, 4], [13, 17, -4]])
    multiplication = ('multiply', [[5, 1, 5], [13, 17, 221]])
    other = ('other', [[1, 6, 99], [12, 12, 12]])
    values = dict([addition, subtraction, multiplication, other])
    system = ('arithmetic', values)

    def badadd(x, _):
        return x + 1

    def badsub(x, _):
        return x - 1

    def mymult(x, y):
        return x * y

    solution = {'add': badadd, 'subtract': badsub, 'multiply': mymult}

    result = list(inconsistencies(solution, system))
    assert len(result) == 4
    assert ('add', [13, 17, (30, 14)]) in result
    assert ('subtract', [13, 17, (-4, 12)]) in result
    assert ('other', [1, 6, (99, None)]) in result
    assert ('other', [12, 12, (12, None)]) in result
