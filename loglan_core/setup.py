# -*- coding: utf-8 -*-
"""
Default engine and Session
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL', None)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, future=True)
