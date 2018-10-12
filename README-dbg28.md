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
