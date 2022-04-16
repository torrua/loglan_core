# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Setting Model
"""
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime

from loglan_core.base import BaseModel
from loglan_core.table_names import T_NAME_SETTINGS

__pdoc__ = {
    'BaseSetting.created': False, 'BaseSetting.updated': False,
}


class BaseSetting(BaseModel):
    """Base Setting's DB Model

    Describes a table structure for storing dictionary settings.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 1, 'last_word_id': 10141,
    'date': datetime.datetime(2020, 10, 25, 5, 10, 20),
    'db_release': '4.5.9', 'db_version': 2}
    ```
    </p></details>
    """
    __tablename__ = T_NAME_SETTINGS

    def __init__(self, db_version: int, db_release: str, last_word_id: int, date: datetime = None):
        super().__init__()
        self.db_version = db_version
        self.db_release = db_release
        self.last_word_id = last_word_id
        self.date = date

    date = Column(DateTime, nullable=True, unique=False)
    """*Last modified date*  
        **dateime.datetime** : nullable=True, unique=False"""
    db_version = Column(Integer, nullable=False, unique=False)
    """*Database version (for old application)*  
        **int** : nullable=False, unique=False"""
    last_word_id = Column(Integer, nullable=False, unique=False)
    """*ID number of the last word in DB*  
            **int** : nullable=False, unique=False"""
    db_release = Column(String(16), nullable=False)
    """*Database release (for new application)*  
            **str** : max_length=16, nullable=False, unique=True"""
