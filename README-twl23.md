# 2018-09-28
    Set up requirements.txt
        - tox (venv manager)
        - pytest (junit for python)
        - coverage (checks code covered)
        - praw (reddit api)

    Guide on venv activation
        - auto activation for mac/linux
        - step by step guide for mac/linux/windows

    Set up tox
        - placeholder tests and command
        - install all dependencies from requirements.txt
        - uses py37

# 2018-10-4
    Updated requirements.txt
        - added kivy 1.10.1

    Set up simple Reddit functionality
        - Created simple way to create OAuth link
        - Utilized refresh token from OAuth link
        - Submitted a post on the private subreddit Postr
        - Currently have all permissions set, may need to consider lowering amount.
        - Need to separate into modules as to OAuth use (one time set up) and refresh token use (always use)

# 2018 10-12
    Reddit functionality
        - Fixed Module use to conform with api
        - Started implementing methods
