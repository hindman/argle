
<!-- 

  # dev-notes: Dev notes
    ## new-venv: Creating a new virtualenv
    ## run-tests: Activate and run tests
    ## version-bump: Version bump
    ## publish: Publish
    ## test-pypi-install: Installing from test pypi
    ## tags-file: Tag file creation

-->

# dev-notes: Dev notes

## new-venv: Creating a new virtualenv

    v='3.14.8'
    p='argle'
    deactivate
    pyenv shell $v && pyenv versions
    mkvirtualenv $p-$v
    pip install -U pip
    pip install -e .[dev,test] && pip list

## run-tests: Activate and run tests

Basic:

    workon argle-3.9.4
    pytest -s -v tests/

With invoke:

    inv test
    inv tox

With tox directly:

    pyenv shell 3.9.4  3.8.9  ...
    tox

## version-bump: Version bump

Edit/commit all changes, including CHANGES and README.

    inv bump --kind major|minor|patch

## publish: Publish

    inv dist [--publish] [--test] [--verbose]

## test-pypi-install: Installing from test pypi

    pip install --index-url https://test.pypi.org/simple/ argle
    pip uninstall short-con
    pip install short-con

## tags-file: Tag file creation

    inv tags

