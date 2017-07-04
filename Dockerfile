from pypy:2-slim
add Pipfile* /app/
workdir /app
env PIPENV_VENV_IN_PROJECT=1
run pip install -U pip pipenv && pipenv install --python pypy
add . /app/
CMD [".venv/bin/python", "app.py", "-d" ]
