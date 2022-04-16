# -*- coding: utf-8 -*-
"""
This module contains functions and variables for initializing application and db
"""

__author__ = "torrua"
__copyright__ = "Copyright 2022, loglan_core project"
__email__ = "torrua@gmail.com"

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL', None)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, future=True)
