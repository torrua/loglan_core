# -*- coding: utf-8 -*-
"""Main app page"""

from loglan_core.setup import Session
session = Session(future=True)

# https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/
# py -m pip install --upgrade build
# py -m build

# py -m pip install --upgrade twine
# py -m twine upload --repository pypi dist/*

if __name__ == "__main__":
    pass
