
<!-- 

# Dev notes
  ## Creating a new virtualenv
  ## Activate and run tests
  ## Version bump
  ## Publish
  ## Installing from test pypi
  ## Tag file creation

-->

# Dev notes

## Creating a new virtualenv

    v='3.14.8'
    p='argle'
    deactivate
    pyenv shell $v && pyenv versions
    mkvirtualenv $p-$v
    pip install -U pip
    pip install -e .[dev,test] && pip list

## Activate and run tests

Basic:

    workon argle-3.9.4
    pytest -s -v tests/

With invoke:

    inv test
    inv tox

With tox directly:

    pyenv shell 3.9.4  3.8.9  ...
    tox

## Version bump

Edit/commit all changes, including CHANGES and README.

    inv bump --kind major|minor|patch

## Publish

    inv dist [--publish] [--test] [--verbose]

## Installing from test pypi

    pip install --index-url https://test.pypi.org/simple/ argle
    pip uninstall short-con
    pip install short-con

## Tag file creation

    inv tags

