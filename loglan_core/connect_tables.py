"""
This module defines the relational mapping between various elements in the database.

It contains the following tables:

- `t_connect_authors`: This table maps authors to their words, creating a many-to-many relationship.
Each row in the table represents a word that is associated with an author.

- `t_connect_words`: This table maps parent words to their child words,
creating a many-to-many relationship. Each row in the table represents a child word
that is associated with a parent word.

- `t_connect_keys`: This table maps definitions to their keys in the database,
creating a many-to-many relationship. Each row in the table represents
a definition that is associated with a key.

Each of these tables is defined with SQLAlchemy's Table construct
and includes indices on key columns to enhance query performance.
"""

from sqlalchemy import Column, ForeignKey, Table, Index

from loglan_core.base import BaseModel as Base
from loglan_core.table_names import (
    T_NAME_AUTHORS,
    T_NAME_KEYS,
    T_NAME_WORDS,
    T_NAME_DEFINITIONS,
    T_NAME_CONNECT_AUTHORS,
    T_NAME_CONNECT_WORDS,
    T_NAME_CONNECT_KEYS,
)

t_connect_authors = Table(
    T_NAME_CONNECT_AUTHORS,
    Base.metadata,
    Column("AID", ForeignKey(f"{T_NAME_AUTHORS}.id"), primary_key=True),
    Column("WID", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True),
    Index("index_AID", "AID"),
    Index("index_WID", "WID"),
)
"""
sqlalchemy.sql.schema.Table: Maps authors to their words in the database.

This table creates a many-to-many relationship between authors and their words.
Each row represents a word that is associated with an author.

Variables:
    T_NAME_CONNECT_AUTHORS (str): The name of the table.
    Column("AID", ForeignKey(f"{T_NAME_AUTHORS}.id"), primary_key=True): 
    The ID column for the author.
    Column("WID", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True): The ID column for the word.
    Index("index_AID", "AID"): An index on the "AID" column to enhance query performance.
    Index("index_WID", "WID"): An index on the "WID" column to enhance query performance.

"""

t_connect_words = Table(
    T_NAME_CONNECT_WORDS,
    Base.metadata,
    Column("parent_id", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True),
    Column("child_id", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True),
    Index("index_parent_id", "parent_id"),
    Index("index_child_id", "child_id"),
)
"""
sqlalchemy.sql.schema.Table: Maps parent words to their child words in the database.

This table creates a many-to-many relationship between parent words and child words.
Each row represents a child word that is associated with a parent word.

Variables:
    T_NAME_CONNECT_WORDS (str): The name of the table.
    Column("parent_id", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True): 
    The ID column for the parent word.
    Column("child_id", ForeignKey(f"{T_NAME_WORDS}.id"), primary_key=True): 
    The ID column for the child word.
    Index("index_parent_id", "parent_id"): An index on the "parent_id" 
    column to enhance query performance.
    Index("index_child_id", "child_id"): An index on the "child_id" 
    column to enhance query performance.
"""

t_connect_keys = Table(
    T_NAME_CONNECT_KEYS,
    Base.metadata,
    Column("KID", ForeignKey(f"{T_NAME_KEYS}.id"), primary_key=True),
    Column("DID", ForeignKey(f"{T_NAME_DEFINITIONS}.id"), primary_key=True),
    Index("index_KID", "KID"),
    Index("index_DID", "DID"),
)
"""
sqlalchemy.sql.schema.Table: Maps definitions to their keys in the database.

This table creates a many-to-many relationship between definitions and their keys.
Each row represents a definition that is associated with a key.

Variables:
    T_NAME_CONNECT_KEYS (str): The name of the table.
    Column("KID", ForeignKey(f"{T_NAME_KEYS}.id"), primary_key=True): 
    The ID column for the key.
    Column("DID", ForeignKey(f"{T_NAME_DEFINITIONS}.id"), primary_key=True): 
    The ID column for the definition.
    Index("index_KID", "KID"): An index on the "KID" column to enhance query performance.
    Index("index_DID", "DID"): An index on the "DID" column to enhance query performance.
"""
