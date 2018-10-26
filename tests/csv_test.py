import csv
import os
from pathlib import Path

from postr.twitter_postr import Twitter

testpath = os.path.join('tests/twitter/graphtest.csv')


def test_csv_setup() -> None:
    t = Twitter()
    t.graphfile = testpath
    t.setup_csv()

    my_file = Path(testpath)
    assert my_file.is_file()


def test_csv_contents() -> None:
    t = Twitter()
    t.graphfile = testpath

    col = []

    with open(t.graphfile, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            col.append(str(row))

    length = len(col)
    assert length == 1
