# webcrawler
This is a fun experiment with asyncio to deal with I/O bound activities

## Setup
Required python version: 3.7.*

Make sure you have python 3.7 installed (otherwise some packages may fail to install and asyncio will puke).

```
$ python --version
> Python 3.7.9
```

Set up a virtual environment:

```
cd <$WEBCRAWLER_PROJECT_DIR>
python -m venv ./venv
source ./venv/bin/activate
```

`poetry` is for python package management:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version 1.1.7

poetry --version
> Poetry version 1.1.7
poetry install
```

This Repo uses `black` and `flake8` for styling, if you wish to commit you'll need to  set up pre-commit hooks:

```
poetry run pre-commit install
```

## Running
```
python -m run_webcrawler <inital_url> -l <OPTIONAL:max_pages_to_visit>
```
This will print the current url and all `http` prefixed urls found in the response.  Each of these will be added to a queue to recurse over.
Once a url is visited it will not be visited again, to prevent loops
If `-l` or `--limit` are not specified, the program will continue to run until interrupted


## Tests
You can find tests in the `tests` dir, and run all tests by running pytest
```
pytest
```
