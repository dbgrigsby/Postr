# 9/28/2018
## Create a pylintrc file
    This enforces style and other metrics
    Notable features:
        max of 5 arguments per funciton
        max of 10 complexity per function
    Run:
       "pylint file.py --rcfile=pylintrc" in /Postr directory

## Create a .vimrc file
    This sets up a dev environment in a user's home directory
    This file is not tracked, but a copy can be found here:
        Note: this link may expire after some time
        https://pastebin.com/raw/xA4BnP99
    Notable features:
        Python autocompletion
        Syntastic plugin:
            Checks for a pylintrc file, and automatically runs it when file is saved.
    Run:
        Automatically loaded when put into the HOME directory

## Create setup.cfg file for flake8
    Notable features:
        Calls pylint for syntax checking
        Allows PEP8 analysis of code
    Run:
        "flake8 file.py"

## Create mypy.ini file for mypy
    Notable features:
        Allows for static type checking with the typing module
        Enforces very strict type checking as defined in mypy.ini
    Run:
        "mypy file.py"
