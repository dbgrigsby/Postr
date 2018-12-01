# 2018-11-30
    Add four new APIs with basic functions to the Task Processor
    Fix the long standing GUI-in-venv bugs
# 2018-11-16
    Finished the listed Slack API Functionality as planned
    Additionally, I made the Task Processor work for the multiple APIs by fixing bugs, and did a demo with Reddit"
# 2018-11-09
    I added the basis of the Slack API
        With 2 supported functions>>
    I also fixed some bugs with the Scheduler
# 2018-11-02
    During this week, I created the task processor for executing a command from a Scheduler instruction,
    This was designed to also be callable from a UI button click
    THis involved reading and integrating all APIs into one task processor
    Additionally fix some misc bugs in other APIs I found while doing it
# 2018-10-26
    During this week, I  will get back on schedule, fix bugs, and cleanup the code.
    This week will also be used for extra testing for discord and the config parser
# 2018-10-19
    Logger
        Add a reusable logger for all devs, with dual file/stdout logging
    Complete Discord API implementation
        Delete bot messages
        Posting images
        Updating bot profile (status)
        Posting announcements
    More specific API:
        Split discord away from general api_interface, first step of the separation
    General
        Style settings tweaks
# 2018-10-12
    Add mypy requirement to tox and update everyone's code to be typing-compliant
    Add authentication and message logging / posting feature to Discord
    Add more precommit hooks for code complexity and style
# 2018-10-05
    Created config parser interface
        Saves config to an .ini file
        Works for any authentication schema, as it lets users add their own key/value pairs
        Make travis cache precommit, saving us 2 minutes per build
# 2018-09-28
    Set up Docker configuration
    Created setup.py for repository info
    Added travis config for automatic builds (untested)
    Wrote developer documentation for Docker
    Write weekly update script for CSEVCS pushes
    Note:
        The Gantt chart lists briefly 'tox' under my responsibilities.
        This was moved to Tommy Lu's responsibilities prior to week 1
