# Hooks in the current pre-commit setup  

`trailing-whitespace`  
* Removes all trailing white spaces from liens based on the type of file
* ex : leave the last two spaces on markdown file lines  

`end-of-file-fixer`  
- Removes newlines from the end of files

`autopep8-wrapper`  
- Automatically formats Python code to conform to the PEP 8 style guide

`check-docstring-first`  
* Checks the placement of docstring in the file (similar to java docs)

`check-json`  
* This hook checks json files for parseable syntax

`check-yaml`  
* This hook checks yaml files for parseable syntax

`debug-statements`  
* Check for debugger imports and py37+ `breakpoint()` calls in python source.

`name-tests-test`  
* This verifies that test files are named correctly

`requirements-txt-fixer`  
* Sorts entries in requirements.txt

`flake8`  
* This hook runs flake8.

`check-ast`  
* Simply check whether the files parse as valid python.

`fix-encoding-pragma`  
* Add # -*- coding: utf-8 -*- to the top of python files

`reorder-python-imports`  
* This hook reorders imports in python files.

`pyupgrade`  
* Automatically upgrade syntax for newer versions.

`add-trailing-comma`
* Automatically add trailing commas to calls and literals.

`no-catchall-except`
* not on the list for some reason

#### To see more pre-commit hooks visit : https://pre-commit.com/hooks.html
