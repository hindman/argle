
<!-- 

# dn-dev-notes: Dev notes
  ## dn-new-venv: Creating a new virtualenv
  ## dn-run-tests: Activate and run tests
  ## dn-version-bump: Version bump
  ## dn-publish: Publish
  ## dn-test-pypi-install: Installing from test pypi
  ## dn-tags-file: Tag file creation

-->

# dn-dev-notes: Dev notes

## dn-new-venv: Creating a new virtualenv

    v='3.14.8'
    p='argle'
    deactivate
    pyenv shell $v && pyenv versions
    mkvirtualenv $p-$v
    pip install -U pip
    pip install -e .[dev,test] && pip list

## dn-run-tests: Activate and run tests

Basic:

    workon argle-3.9.4
    pytest -s -v tests/

With invoke:

    inv test
    inv tox

With tox directly:

    pyenv shell 3.9.4  3.8.9  ...
    tox

## dn-version-bump: Version bump

Edit/commit all changes, including CHANGES and README.

    inv bump --kind major|minor|patch

## dn-publish: Publish

    inv dist [--publish] [--test] [--verbose]

## dn-test-pypi-install: Installing from test pypi

    pip install --index-url https://test.pypi.org/simple/ argle
    pip uninstall short-con
    pip install short-con

## dn-tags-file: Tag file creation

    inv tags

