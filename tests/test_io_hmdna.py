from eigen.io.hmdna import unzip
from eigen.io.hmdna import system


def test_HMDNA_zip():
    (name, tests) = unzip("tests/hmdna/FooBar.zip")
    assert name == "FooBar"
    assert len(tests) == 3
    assert tests[0] == ['yohoho', 3, 'o']
    assert tests[1] == ['yohoho', 2, 'oh']
    assert tests[2] == ['bottle', 2, 'at']


def test_HMDNA_bad_zip():
    """Some HMDNA zip files have top directory named
    differently from zip file.
    """
    (name1, tests1) = unzip("tests/hmdna/FooBar.zip")
    (name2, tests2) = unzip("tests/hmdna/BarBaz.zip")
    assert name1 == 'FooBar'
    assert name2 == 'BarBaz'
    assert tests2 == tests1


def test_HMDNA_lists():
    """Handle space-separated lists and homogenize."""
    (name, tests) = unzip("tests/hmdna/PatMat.zip")
    assert name == "PatMat"
    assert len(tests) == 3
    assert tests[0] == ['ATAT', 'GATATATGCATATACTT', [1, 3, 9]]
    assert tests[1] == ['ACAC', 'TTTTACACTTTTTTGTGTAAAAA', [4]]
    assert tests[2] == ['ATA', 'ATATATA', [0, 2, 4]]


def test_system():
    """Read an entire system from a directory of zip files."""

    name, sys = system('tests/hmdna')
    assert name == 'hmdna'
    assert 'FooBar' in sys.keys()
    assert 'PatMat' in sys.keys()
    tests = sys['BarBaz']
    assert tests[0] == ['yohoho', 3, 'o']
    assert tests[1] == ['yohoho', 2, 'oh']
    assert tests[2] == ['bottle', 2, 'at']
