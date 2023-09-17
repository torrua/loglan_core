# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Connection Table Models
"""
from sqlalchemy import Column, ForeignKey, Table
from loglan_core.base import BaseModel as Base
from loglan_core.table_names import T_NAME_AUTHORS, T_NAME_KEYS, T_NAME_WORDS, T_NAME_DEFINITIONS, \
    T_NAME_CONNECT_AUTHORS, T_NAME_CONNECT_WORDS, T_NAME_CONNECT_KEYS

t_connect_authors = Table(
    T_NAME_CONNECT_AUTHORS, Base.metadata,
    Column('AID', ForeignKey(f'{T_NAME_AUTHORS}.id'), primary_key=True),
    Column('WID', ForeignKey(f'{T_NAME_WORDS}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseAuthor` and `BaseWord` objects"""

t_connect_words = Table(
    T_NAME_CONNECT_WORDS, Base.metadata,
    Column('parent_id', ForeignKey(f'{T_NAME_WORDS}.id'), primary_key=True),
    Column('child_id', ForeignKey(f'{T_NAME_WORDS}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
(parent-child) between `BaseWord` objects"""

t_connect_keys = Table(
    T_NAME_CONNECT_KEYS, Base.metadata,
    Column('KID', ForeignKey(f'{T_NAME_KEYS}.id'), primary_key=True),
    Column('DID', ForeignKey(f'{T_NAME_DEFINITIONS}.id'), primary_key=True), )
"""`(sqlalchemy.sql.schema.Table)`: 
Connecting table for "many-to-many" relationship 
between `BaseDefinition` and `BaseKey` objects"""
