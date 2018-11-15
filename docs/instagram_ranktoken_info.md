# What is a rank token
    Every instagram user has a random id associated with them called a rank token.
    This token allows the user to perform GET requests on Instagram's platform.

# How to find your rank token
    Go to the instagram homepage. Next, click the search bar, and start typing some letters.
    In your browser, inspect element, and navigate to the area that shows current GET requests.
    Look for the request dealing with /instagram.com/web/search/topearch.
    Your rank token will be in this request.

# How to put the rank token in the config file
    Open up postr_config.ini. Make a key for 'RANK_TOKEN' and put your rank token as a value,
    in this format: &rank_token=0.{token here}

    For eaxmple, the .ini file should look like this regarding Instagram rank tokens:
    RANK_TOKEN = &rank_token=0.23423818334234
