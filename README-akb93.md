# 10/5/2018
## Create dbsetup.py
    Created a setup file for first-time users who download/clone the postr project
    Running this file creates a database to hold scheduling operations, called
    master_schedule.sqlite.
    Job:
        Holds data for arbitrary text/media posts, with an optional field for
        any additional info that social media sites require
    Bio:
        Holds data for social media bios, with the option of using a
        display name instead of one's first and last name
    Person:
        Holds data for an arbitrary person, which can be linked from
        a bio row through a foreign key
    DailyJob:
        Holds data for an arbitrary job (connected through a foreign key).
        This job can have set intervals and frequencies, and will continue to
        operate until its frequency limit for the day is met.
    MonthlyJob:
        Holds data for an arbitrary job (connected through a foreign key).
        This job can have set intervals and frequenceis, and will continue to
        operatre until its frequency limit for the month is met.
    CustomJob:
        Holds data for an arbitrary job(connected through a foreign key).
        Can be executed on a custom date. The purpose of this table is to hold
        jobs that have separate use cases from a daily and monthly job.

    I also made Inserter.py:
        Given a conneciton to master_schedule.py, inserts rows for
        Person, Job, CustomJob, and Bio tables. The rest of the tables will
        be implemented upon further discussion.





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
