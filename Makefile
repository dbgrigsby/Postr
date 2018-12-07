
# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

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
# link : https://blog.horejsek.com/makefile-with-python/
