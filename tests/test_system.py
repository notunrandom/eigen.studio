from eigen.system import solve
from eigen.system import solution
from eigen.system import solutions


def test_solve_empty_system():
    system = {}
    solution = {}
    (solved, unsolved) = solve(system, solution)
    assert solved == unsolved == {}


def test_solve_all():

    system = {'add': [[13, 17, 30]]}

    def myadd(x, y):
        return x + y

    solution = {'add': {myadd}}
    (solved, unsolved) = solve(system, solution)

    assert unsolved == {}
    assert solved == {'add': {myadd}}


def test_solve_some():

    addition = ('add', [[5, 1, 6], [13, 17, 30]])
    subtraction = ('subtract', [[5, 1, 4], [13, 17, -4]])
    multiplication = ('multiply', [[5, 1, 5], [13, 17, 221]])
    other = ('other', [[1, 6, 99], [12, 12, 12]])
    system = dict([addition, subtraction, multiplication, other])

    def badadd(x, _):
        return x + 1

    def badsub(x, _):
        return x - 1

    def mymult(x, y):
        return x * y

    solution = {'add': {badadd}, 'subtract': {badsub}, 'multiply': {mymult}}
    (solved, unsolved) = solve(system, solution)

    assert solved == {'multiply': {mymult}}
    assert len(unsolved) == 3
    assert unsolved['add'] == {badadd: [[13, 17, (30, 14)]]}
    assert unsolved['subtract'] == {badsub: [[13, 17, (-4, 12)]]}
    assert unsolved['other'] == {}


@solution(lambda _: ('mytestsystem', 'fun1'))
def myfun1(string):
    return 2 * string


@solution(lambda _: ('mytestsystem', 'fun2'))
def myfun2(x, y):
    return x * y


def test_solution():
    system = {'fun1': [['yo', 'yoyo'], ['xyz', 'xyzxyz']],
              'fun2': [[1, 2, 2], [3, 7, 21], [0, 31, 0]]}
    sol = solutions('mytestsystem')
    (solved, unsolved) = solve(system, sol)
    assert unsolved == {}
    assert solved == {'fun1': {myfun1}, 'fun2': {myfun2}}


@solution()
def fun1(x):
    return 3 * x


@solution()
def fun2(x, y):
    return x + y


def test_implicit_solution():
    system = {'fun1': [['yo', 'yoyoyo'], [7, 21]],
              'fun2': [[1, 2, 3], [3, 7, 10], [0, 31, 31]]}
    sol = solutions(__name__)
    (solved, unsolved) = solve(system, sol)
    assert unsolved == {}
    assert solved == {'fun1': {fun1}, 'fun2': {fun2}}
