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
        - Utilized config for secret keys
        - Created class for Reddit usage
        - Typed methods

# 2018 10-18
	Updated Makefile
		- Now properly uses venv
		- Added creation of venv on windows and other OSes
	Reddit functionality
		- Added creating wiki pages (subreddit bio essentially)
		- Added editing wiki pages
		- Added functionality for returning a list of wiki pages from a subreddit
		- Added basic foundation of parsing subreddit posts
		-

# 2018 10-25
	Set up simple YouTube functionality
		- Added google requirements to requirements
		- Set up basic template
		- Generated link
		- Utilized refresh token

# 2018 11-2
	YouTube functionality
		- Utilized token to upload video. Added basis for adding videos.
		- Converted sample code found here https://developers.google.com/youtube/v3/docs/videos/insert#usage
		- Need to convert video uploading service into a more serviceable and integrated version.
		- Need to save refresh token.

# 2018 11-9
	YouTube functionality
		- Set up refresh token function
		- Reused refresh token generated
		- Added functionality to provide statistics
		- Need to figure out how to properly integrate YouTube (post values are upload and there is little need to post)

# 2018 11-16
	YouTube functionality
		- Integrated functionality for add, delete, and get subscriber count (equivalent to like count) onto api interface
		- Commented on implementation reasons behind several interface functions
		- Added typing to all functions and interface functions, with relevant sample code from google typed to Any if type unable to be determined
		- Need to figure out still how to properly integrate into gui functionality, be it through disabling and adding option to post link of uploaded
			- to other sites.

# 2018 11-23
	Thanksgiving Break

# 2018 11-30
	Assisted in creation of the Poster
	YouTube functionality
		- Added a way for the user to retrieve recent uploaded video_ids
			- Allows for displaying of uploaded videos
			- Allows for access to uploaded videos to delete or re upload

# 2018 12-7
	Assisted Adam Beck with creation of some of the Poster (around 10-20% helped such that 1-2 hours were done)
	Set-up Sphinx documentation
		- Setup Makefile to allow for `make help` for Sphinx documentation setup
		- The most basic Sphinx documentation setup is `make html`
		- Once this is called, the folder containing the documentation from the main Poster folder is `/_build/html`. Open `index.html` for the homepage.
		- Generated rst files for all modules utilizing apigen (library is not included in venv because it is a one-time make for each module) using command `sphinx-apidoc postr -o .` in the main Postr folder.
			- Note that conf.py is setup to point to our `postr` module folder.
	All api coding has been finished so mostly documentation touch ups and poster assistance.
