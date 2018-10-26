from postr.twitter_postr import Twitter


def test_polarity() -> None:
    assert Twitter.polarity('test') == 0
    assert Twitter.polarity('positive') > 0
