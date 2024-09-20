# Loglan Core

![Codecov](https://img.shields.io/codecov/c/github/torrua/loglan_core?logo=Codecov&logoColor=%23F01F7A&label=codecov)
![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/g/torrua/loglan_core/main?logo=Scrutinizer%20CI&logoColor=%238A9296&label=Scrutinizer%20CC&link=https%3A%2F%2Fscrutinizer-ci.com%2Fg%2Ftorrua%2Floglan_core%2F%3Fbranch%3Dmain)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/torrua/loglan_core?logo=Code%20Climate)
![pylint](https://img.shields.io/badge/PyLint-9.95-yellow?logo=python&logoColor=white)
[![Pytest](https://github.com/torrua/loglan_core/actions/workflows/pytest.yml/badge.svg)](https://github.com/torrua/loglan_core/actions/workflows/pytest.yml)
![Bandit Status](https://img.shields.io/github/actions/workflow/status/torrua/loglan_core/bandit.yml?label=bandit)
![Black Status](https://img.shields.io/github/actions/workflow/status/torrua/loglan_core/black.yml?label=Black&labelColor=black)

![PyPI - Downloads](https://img.shields.io/pypi/dm/loglan_core?color=yellow)
![PyPI - Version](https://img.shields.io/pypi/v/loglan-core?logo=PyPi&logoColor=%23FFFFFF)
![GitHub License](https://img.shields.io/github/license/torrua/loglan_core)



# SQLAlchemy Database Model for Loglan Dictionary

This project represent a SQLAlchemy database model for the dictionary of [constructed language Loglan](http://www.loglan.org/). 
It contains schemas for information about words, authors, lexical events, and even more.

![SQL LOD Schema](.images/LOD.pgerd.png)

## Features
Provides a structured SQLAlchemy model for the Loglan dictionary.
Includes classes for handling words, authors, lexical events, and more.
Can be easily integrated into Python projects to provide Loglan language support.

## Prerequisites

Before installing, ensure you have the following software installed on your system:

- Python 3.10+
- pip (Python package manager)

## Installation
You can install Loglan-Core using pip:
```bash
pip install Loglan-Core
```

## Usage
After installing the package, you can use it as follows:

```bash
from loglan_core import Word, Type, Event, Key
# your code here...
```
For more details please see [Intro](examples/intro.md), [Word](examples/word.md) and [WordSelector](examples/word_selector.md) documentation with examples.

## License
Loglan-Core is licensed under the MIT license.