.PHONY: prepare-dev test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python2
	
# will proboably need to add more installations later 
# might just be 
prepare-dev:
    sudo apt-get -y install python3.5 python3-pip
    python3 -m pip install virtualenv 
    make venv

# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
venv: $(VENV_PATH)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
    test -d $(VENV_PATH) || virtualenv -p python2 $(VENV_PATH)
    ${PYTHON} -m pip install -U pip
    ${PYTHON} -m pip install -e .
    touch $(VENV_PATH)/bin/activate


test: venv
    ${PYTHON} -m pytest

lint: venv
    ${PYTHON} -m pylint
    ${PYTHON} -m mypy

run: venv
    ${PYTHON} app.py

doc: venv
    $(VENV_ACTIVATE) && cd docs; make html
	
# link : https://blog.horejsek.com/makefile-with-python/