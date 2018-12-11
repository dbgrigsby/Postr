.PHONY: install

FOLDER :=
ifeq ($(OS),Windows_NT)
	FOLDER:=Scripts
else
	FOLDER:=bin
endif

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/$(FOLDER)/activate
PYTHON=${VENV_NAME}/$(FOLDER)/python

# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
install: create activate

sphinx-docs: activate
	rm -rf docs/source/
	rm -rf docs/_build/
	sphinx-apidoc -o docs/source/ postr
	sphinx-build -M html docs/ docs/_build

create:
ifeq ($(OS),Windows_NT)
	virtualenv venv
else
	python3 -m venv venv
endif

activate:
	source $(VENV_NAME)$(VENV_PATH)/$(FOLDER)/activate; \
	$(VENV_NAME)$(VENV_PATH)/$(FOLDER)/pip install -r prerequirements.txt; \
	$(VENV_NAME)$(VENV_PATH)/$(FOLDER)/pip install -r requirements.txt; \

test: activate
	${PYTHON} -m tox; \

run: activate
	${PYTHON} postr/app.py \

clean:
	rm -rf venv

twitter: activate
	${PYTHON} -m postr.twitter_postr \

setupTextblob: activate
	${PYTHON} -m textblob.download_corpora \

database: activate
	${PYTHON} -m scripts.dbsetup \

gui: activate
	${PYTHON} -m postr.main

gui2: activate
	${PYTHON} -m postr.schedule.reader & ${PYTHON} -m postr.main2 && sudo killall python
# link : https://blog.horejsek.com/makefile-with-python/
