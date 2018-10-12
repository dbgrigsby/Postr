# Holds fixtures
# https://stackoverflow.com/questions/34466027/in-py-test-what-is-the-use-of-conftest-py-files
# http://mcs.une.edu.au/doc/python3-pytest/html/en/fixture.html
import pytest


@pytest.fixture(scope='module')
def add() -> int:
    return 2 + 3
