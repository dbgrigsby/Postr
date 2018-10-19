.PHONY: run
FOLDER :=
ifeq ($(OS),Windows_NT)
	FOLDER:=scripts
else
	FOLDER:=bin
endif

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/$(FOLDER)/activate
PYTHON=${VENV_NAME}/$(FOLDER)/python3

# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
venv:
	$(VENV_PATH)/$(FOLDER)/activate
	$(VENV_NAME)/$(FOLDER)/activate: setup.py
	test -d $(VENV_PATH) || virtualenv -p python3 $(VENV_PATH)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	touch $(VENV_PATH)/$(FOLDER)/activate

test: venv
	${PYTHON} -m pytest

run: venv
	${PYTHON} postr/app.py

precommit: venv
	pre-commit run --all-files

clean:
	rm -rf venv

twitter:
	python -m postr.twitter_postr

setupTextblob:
	python -m textblob.download_corpora

# link : https://blog.horejsek.com/makefile-with-python/
