# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Syllable Model
"""
from sqlalchemy import Column, String, Boolean

from loglan_core.base import BaseModel
from loglan_core.table_names import T_NAME_SYLLABLES

__pdoc__ = {
    'BaseSyllable.created': False, 'BaseSyllable.updated': False,
}


class BaseSyllable(BaseModel):
    """Base Syllable's DB Model

    Describes a table structure for storing information about loglan syllables.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 37, 'name': 'zv', 'type': 'InitialCC', 'allowed': True}

    {'id': 38, 'name': 'cdz', 'type': 'UnintelligibleCCC', 'allowed': False}
    ```
    </p></details>
    """

    __tablename__ = T_NAME_SYLLABLES

    def __init__(self, name: str, type: str, allowed: Boolean = None):
        super().__init__()
        self.name = name
        self.type = type
        self.allowed = allowed

    name = Column(String(8), nullable=False, unique=False)
    """*Syllable itself*  
            **str** : max_length=8, nullable=False, unique=False"""
    type = Column(String(32), nullable=False, unique=False)
    """*Syllable's type*  
            **str** : max_length=8, nullable=False, unique=False"""
    allowed = Column(Boolean, nullable=True, unique=False)
    """*Is this syllable acceptable in grammar*  
            **bool** : nullable=True, unique=False"""
