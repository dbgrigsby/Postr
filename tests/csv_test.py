import csv
from pathlib import Path

from postr.twitter_postr import Twitter


def test_csv_setup() -> None:
    t = Twitter()
    testpath = 'graphtest.csv'
    t.graphfile = testpath
    t.setup_csv()

    my_file = Path(testpath)
    assert my_file.is_file()


def test_csv_contents() -> None:
    t = Twitter()
    testpath = 'graphtest.csv'
    t.graphfile = testpath

    col = []

    with open(t.graphfile, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            col.append(str(row))

    length = len(col)
    assert length == 1


def test_polarity() -> None:
    assert Twitter.polarity('test') == 0
    assert Twitter.polarity('positive') > 0
