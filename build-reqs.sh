#!???/???/???
# shebang venv is a WIP atm

pipreqs --ignore bin,etc,include,lib,lib64 --force --savepath=requirements.in && pip-compile