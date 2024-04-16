"""
For coverage:
pytest tests/test_hello.py -v --cov=src/ensemble --cov-report term-missing
"""

# import .hello as hh
# import hello as hh
# from ptg import hello as hh
from ensemble import hello as hh


def test_hello():
    """Tests that the string returned from 'hello world' is as excpected."""
    known = "Hello world!"
    found = hh.hello()

    assert found == known


def test_adios():
    """Tests that the string returned from 'adios' is as excpected."""
    known = "Bye"
    found = hh.adios()

    assert found == known
