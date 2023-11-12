from eigen.system import solve
from eigen.system import solves
from eigen.system import solution
from eigen.system import solutions
from eigen.system import match
from eigen.system import match_key
from eigen.system import norm
import my_system
import my_system_2


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


@solves('mytestsystem', 'fun1')
def myfun1(string):
    return 2 * string


@solves('mytestsystem', 'fun2')
def myfun2(x, y):
    return x * y


def test_solves():
    system = {'fun1': [['yo', 'yoyo'], ['xyz', 'xyzxyz']],
              'fun2': [[1, 2, 2], [3, 7, 21], [0, 31, 0]]}
    sol = solutions('mytestsystem')
    (solved, unsolved) = solve(system, sol)
    assert unsolved == {}
    assert solved == {'fun1': {myfun1}, 'fun2': {myfun2}}


@solution
def fun1(x):
    return 3 * x


@solution
def fun2(x, y):
    return x + y


def test_solution():
    system = {'fun1': [['yo', 'yoyoyo'], [7, 21]],
              'fun2': [[1, 2, 3], [3, 7, 10], [0, 31, 31]]}
    sol = solutions(__name__)
    (solved, unsolved) = solve(system, sol)
    assert unsolved == {}
    assert solved == {'fun1': {fun1}, 'fun2': {fun2}}


def test_match_easy():
    systems = {'my_system': {'my_abc': [[1, 2]], 'my_xyz': [['foo', 'oof']]},
               'other': {'foo': [[1, 2]], 'bar': [[2, 1]]}}
    system, solution = match(systems, my_system)
    assert system == systems['my_system']
    assert solution == {'my_abc': {my_system.my_abc},
                        'my_xyz': {my_system.my_xyz}}
    solved, unsolved = solve(system, solution)
    assert unsolved == {}
    assert solved == solution


def test_match_wrong_arity():
    systems = {'my_system': {'my_abc': [[1, 2]], 'my_xyz': [['yo', 'oy', 3]]},
               'other': {'foo': [[1, 2]], 'bar': [[2, 1]]}}
    system, solution = match(systems, my_system)
    assert system == systems['my_system']
    assert solution == {'my_abc': {my_system.my_abc}}
    solved, unsolved = solve(system, solution)
    assert len(unsolved) == 1
    assert unsolved['my_xyz'] == {}
    assert solved == solution


def test_norm():
    tests = [('name', 'name'),
             ('name30', 'name'),
             ('name_30', 'name'),
             ('my_name', 'my_name'),
             ('my-name', 'my_name'),
             ('myName', 'my_name'),
             ('My Name', 'my_name'),
             ('my name', 'my_name'),
             ('my$name', 'myname'),
             ('03-MyName', 'my_name')
             ]
    for inp, out in tests:
        assert norm(inp) == out


def test_match_key():
    d = {'my_a': 1, 'my_b': 2}
    assert match_key(d, 'my_a')['my_a'] == 1
    assert match_key(d, 'myA')['my_a'] == 1
    assert match_key(d, 'myB')['my_b'] == 2
    assert match_key(d, 'my_a2')['my_a'] == 1
    assert match_key(d, 'my_a_2')['my_a'] == 1
    assert match_key(d, 'foo') == {}


def test_match_camel_under():
    systems = {'MySystem': {'MyAbc': [[1, 2]], 'myXyz': [['yo', 'oy']]}}
    system, solution = match(systems, my_system)
    assert system == systems['MySystem']
    assert solution == {'MyAbc': {my_system.my_abc},
                        'myXyz': {my_system.my_xyz}}
    solved, unsolved = solve(system, solution)
    assert unsolved == {}
    assert solved == solution


def test_match_multi():
    systems = {'my_system': {'my_abc': [[1, 2]], 'my_xyz': [['foo', 'oof']]},
               'other': {'foo': [[1, 2]], 'bar': [[2, 1]]}}
    system, solution = match(systems, my_system_2)
    assert system == systems['my_system']
    assert solution == {'my_abc': {my_system_2.my_abc, my_system_2.my_abc_2},
                        'my_xyz': {my_system_2.my_xyz, my_system_2.my_xyz7}}
    solved, unsolved = solve(system, solution)
    assert unsolved == {}
    assert solved == solution
