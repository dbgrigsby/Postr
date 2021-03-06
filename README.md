12/7/2018:
- The team will finish up any work and/or unit tests left to do for their APIs.
- The team will finish connecting the GUI to the backend code.
- Members of the team not doing any of the above tasks will work on the intersections poster and 10-20 page final document

11/30/2018:
- The team will individually complete their implementation / GUI integration of the second group of APIs.
- The User Experience Engineer will create GUIs for each of the APIs created last week
- Those who finish early will work on documenting the project's exact usage (10-20 pages), write in-program guides for users, clean up the interfaces and hide all possible errors behind screens that a casual user would be able to understand.

11/23/2018:
- Gap week: Thanksgiving

11/16/2018:
- The team will finish implementing their second set of APIs.
- If implementation is finished, then they will begin testing for their second API.
- The User Experience Engineer begin hooking up last week's development to the frontend.


11/9/2018:
- The team will each begin implementation of their second set of APIs.
- This is predicted to go much faster, but overlaps with scheduler development, so is allotted one week.
- The User Experience Engineer will create a GUI for the Scheduling system.


11/2/2018:
- The team will pull back together and build the Scheduler, which will allow a user to schedule an arbitrary event for a specific API.
- We will need a database to store the scheduling events, and  way for the program to run 'in the background' (likely minimized to a system tray).
- A communication channel (MQTT?) will be created between the event-based part of the app, the frontend, and the long-running scheduler application, so that there is no intolerably long wait time for communication between the two parts of the app, or either and the database. The system should be tested.
- Those not working on the scheduler will be working on their individual APIs


10/26/2018:
- During this week, the team will get back on schedule, fix bugs, and cleanup the code.  This week will also be used for extra testing.  We will work ahead if needed.
- During this week the User Experience Engineer will finish adding last week's work, the finished APIs 1-4, to the GUI.


10/19/2018:
- Each team member implemented the final version of their API
- The User Experience Engineer begin hooking up last week's development to the frontend.


10/12/2018:
- User Experience Engineer Only:  Create the different GUI pages and a navigation system, so that each developer can work relatively independantly on an API.
- This week will create a base format for a social media platform GUI with buttons and icons. These buttons will be hooked up to the abstract class/interface that all API classes will conform to, and won't actually do anything. A beta of the stats tracking page should exist here, which will read data from the database. A GUI wizard (or similar) process for logging into / authenticating an acount should be created, but again, will not do anything.
- Each team member will take hold of one Social Media platform, listed in their individual Gantt chart, and set up authentication + one other feature. Users should be able to authenticate and perform one media action after this is complete. Tests will be created for work done in this stage.


10/5/2018:
- Create, setup and provide interfaces for the database (to be used with scheduler or stat tracking), the json config where auth keys are stored, and project settings. Create class layout for the project, including all relevant interfaces. Kivy should be runnable, although the GUI does not need to show anything useful. This is just for being able to call any backend function from Kivy


9/28/2018:
- Create repository on Github. Create dockerfile for project to get cross-platform compatibility. Setup project python virtual environment, (with activator), requirements.txt. Setup precommit to ensure style. Set up Tox for testing python. Create a Makefile for ease of use. Choose and enable a code coverage library for test coverage. Create gitignore. Create python auto linting setup (pylint, flake8, mypy) for precommit. Create folder structure


9/20/18 and prior:
- This was before the git server was setup.
- Worked on SRS (requirements document), preliminary
  research, and Gantt charts.
