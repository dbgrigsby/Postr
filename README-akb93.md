#11/9/2018
## Refactor previous week's Twitter code
    I moved a bio method to the main twitter module
    so that the scheduler can dynamic dispatch this method.

## Implement Instagram media upload operations
    Implemented posting media/photos for an Instagram account

## Implement Instagram bio operations
    Created functions to handle all types of input for bio updating,
    as well as string formatting for certain operations
    (e.g. phone numbers)

##  Misc
    Add instagram tokens to the config parser, as well as Implemented
    the api interface.

#11/2/2018
## Implement schedule reader
    Reads the database scheduler, and returns a JSON object of current
    tasks to schedule.
## Implement schedule writer
    Writes to the database, using datetime's timestamp to provide
    easy comparison for the reader operations
## Scheduler
    Did various work on the setup db file, fixed minor errors
    Refactored the database schema to accomodate job ID's and
    also multiple platforms per job

#10/26/2018
## Implement AI testing
    Found in AI_test.py
    Tested the polarity of sentences
    Tested the sentiment conversion from a sample graphfile
    Tested sentiment output for a blobfile

## Implement CSV testing
    Found in csv_test.py
    Tested read column reading, ignoring the headers
    Tested CSV setup for the twitter streaming
    Tested CSV contents of the setup file

#10/19/2018
## Implement twitter operations
    Implemented methods for removing posts, getting
    follower information, posting a photo, and posting text.

## Impelement stream limits
    Impelemented a limit on the hashtag streaming, so the streamer
    stops after a set amount of tweets found.

## create twitter info file
    Implements getters for all info about a user profile, such as
    their twitter ID, latest tweet, tweet from a given ID, latest
    favorites, and retweet information.

## create twitter bio file
    Impelements getters and updaters for bio operations, such as
    updating ones bio, updating their name, and getting name and
    bio information.

## create twitter graphing file
    Implemented a graphing file in CSV format, that stores datetime
    info about a streamed tweets

## created a twitter blob file
    Impelemnted a blob file, containing textblob sentiment analysis
    on streamted tweets

## overall sentiment analysis, pagination, and graphing
    After filtering realtime tweets for the streamer, I was able to
    load the tweet JSON object and extract the text of the tweet. I
    implemented a streamlimed proccess for storing datetime info,
    using a rudimentary AI to analyze the sentiment positivity, and
    graph the positivity over time.

#10/12/2018
## Create twitter streamer file
    Filters realtime tweets based on a hashtag:
        Continuously streams tweets in real time, no delay is detected
        Writes results to an output file called tweets.txt
    Since I gave myself next week to implement Pagination and Posting operations, I will
    delay these until next week.
    Also, I worked on integrating pylint and mypy into precommit:
        Our team cannot "git commit" anything until the pylint and mypy
        syntax and style checkers detect zero erros across every file.
        This ensures that our files are consistent and maintainable.
    I fixed all week1-3 code that was prior to my code, to conform with the pylint and
    mypy precommit checks. Now, our team is up-to-date regarding this.

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
