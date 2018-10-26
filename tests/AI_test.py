import csv
import os

from pathlib import Path
from postr.twitter_postr import Twitter


t = Twitter()
t.graphfile = os.path.join('tests/twitter/graphtest2.csv')


def test_polarity() -> None:
    assert Twitter.polarity('test') == 0
    assert Twitter.polarity('positive') > 0


def test_sentiment() -> None:
    t.blobfile = os.path.join('tests/twitter/blobtest.csv')
    t.analyzeSentiment()

    my_file = Path(t.blobfile)
    assert my_file.is_file()

    scores = []

    with open(t.blobfile, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        i = 0

        for row in reader:
            if i > 0:
                scores.append(int(row[1]))
            i += 1

    total = sum(scores)
    assert total != 0
