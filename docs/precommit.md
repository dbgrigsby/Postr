# Installing pre-commit

`$ virtualenv venv`  
`$ . venv/bin/activate`   // for windows `venv\Scripts\activate`  
`$ pip install pre-commit`  
`$ pre-commit install`  
`$ pre-commit run --all-files`  


Following these instructions sets up precommit. Then, when you try to commit in the virtual environment with normal `git commit -m ""`, pre-commit check will start.

Instructions found here : https://github.com/pre-commit/demo-repo
