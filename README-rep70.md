# September 28, 2018
  - Created basic kivy app
    - Set up base application
    - Added tabs for each future feature
    - Runs locally using Cython 0.28.5 and Kivy 1.9.1
  - Researched how to dockerize kivy app
    - Modified Dockerfile to included Cython, one of the dependencies required for Kivy
    - Have tried using Cython versions 0.20 through 0.28.5
    - Have tried using Kivy versions 1.09 through 1.10
    - After reading countless articles and sifting through a lot of code I am currently unalbe to dockerize our kivy application, however there are a few other things to continue trying next week to make the application work
  - Created Kivy documentation in Docs. Will be updated as the project progresses

# October 5, 2018
  - Updated Kivy documentation in Docs to include more detail and steps for installing and running
  - Added layouts to each feature tab of the application
  - Added spinner menus to each layout
  - Began text and set up for the layout of the Profile page
    - Username
    - Change password
  - Updated requirements.txt
    - added kivy 1.10.1
  - Updated tox.ini
  - Added prerequirements.txt

# October 12, 2018
  - Changed background color to white for tab content panels
  - Changed text color from white to black for greater visibility
  - Added text input boxes for profile updates
  - Added search and replace option to update tab
  - Added event options and checkboxes to events tab
  - Added heading to post tab
  - Refactored and organized the layout of each of the tabs

# October 19, 2018
  - Added to the performance tab
    - Follower count and total likes
  - Started method to add follower count and total likes to performance tab based on selected site
  - Looked into how code for the four APIs from round one was written
    - Implemented interface or not
    - Necessary imports, what methods were left out, how to call etc.
  - Researched connecting kivy frontend to a complex backend

# October 26, 2018
  - Broke out spinners to allow for individual access
  - Named and redefined all of the text input variables to all for easy text access
  - Restructured how the checkboxes were created to allow for future integration
  - Added to and modified the performance method
    - Calls appropriate method for each site to get follower count and total likes
    - Values set ot 0 represent APIs that are not yet implemented
  - Basic structure for events method
  - Basic structure for updates method
    - Cannot be implemented until additions are made to individual APIs and the API interface
  - Basic structure for method to update user profile
    - Considering breaking out sure profile into a new data structure, looking into kivy and passwords/ account information
  ** Some emthods commented out due to the inability to fully implement. These methods were triggering our mypy testing and weren't able to be changed

# November 2, 2018
  - Modified performance method so that it passes all pre-commit tests and builds
  - Updated tox.ini to allow for methods of greater complexity
  - Reorganized inputs from individual methods to overall program
  - Hooked up youtube API to performance method
  - Modified event method framework to instead work for immediate posting
  - Added another method to later hook up to the scheduler for scheduling posts that are not immediate
  - Added more options to post tab
    - What kind of post
    - When the post should be created (immediately or scheduled)
    - Text input to allow for date and time to be added once the scheduler is implemented
