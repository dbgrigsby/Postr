# Creating a Virtual Environment
-  https://docs.python.org/3/library/venv.html

# To set up virtual environment (Mac/Linux):
1. `python3.7 -m venv venv`
2.  `source venv/bin/activate`
3.  `pip install -r requirements.txt`
4. start developing
5. run `deactivate` when finished
6. the `.git` folder should be in the same working directory as `venv`

# To set up virtual environment (Windows) :
1. Install to your python `pip install virtualenv`
2. Setup environment folder `virtualenv venv`
3. Start virtual environment `source venv/Scripts/activate`
4. `pip install -r requirements.txt`
5. start developing
6. run `deactivate` when finished
7. the `.git` folder should be in the same working directory as `venv`

# Adding new packages
1. `pip install (new package)`
2. `pip freeze > requirements.txt`
3.  everyone else rerun `pip install -r requirements.txt`

# To setup automatic cd into activation
1. `copy script bashrc.md`
2. Paste it into your .bashrc file
3. Ensure that it uses the same folder name `venv` as your virtual environment