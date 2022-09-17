# -*- coding: utf-8 -*-
"""
Default engine and Session
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL', "sqlite://")
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine, future=True))
