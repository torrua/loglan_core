# -*- coding: utf-8 -*-
# pylint: disable=C0303

"""
This module contains a basic Event Model
"""
from __future__ import annotations

from sqlalchemy import Column, String, Date, Text
from sqlalchemy import select
from sqlalchemy.orm import relationship, Session

from loglan_core.base import BaseModel
from loglan_core.table_names import T_NAME_EVENTS

__pdoc__ = {
    'BaseEvent.created': False, 'BaseEvent.updated': False,
}


class BaseEvent(BaseModel):
    """Base Event's DB Model

    Describes a table structure for storing information about lexical events.

    <details><summary>Show Examples</summary><p>
    ```python
    {'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.',
     'date': datetime.date(1975, 1, 1), 'annotation': 'Initial', 'name': 'Start', 'id': 1}

    {'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary,
    identified ones that the parser did not recognize as words',
    'date': datetime.date(2016, 1, 15), 'annotation': 'Randall Cleanup',
    'name': 'Randall Dictionary Cleanup', 'id': 5}
    ```
    </p></details>
    """
    __tablename__ = T_NAME_EVENTS

    def __init__(self, date, name, definition, annotation, suffix):
        super().__init__()
        self.date = date
        self.name = name
        self.definition = definition
        self.annotation = annotation
        self.suffix = suffix

    date = Column(Date, nullable=False, unique=False)
    """*Event's starting day*  
        **dateime.date** : nullable=False, unique=False"""
    name = Column(String(64), nullable=False, unique=False)
    """*Event's short name*  
        **str** : max_length=64, nullable=False, unique=False"""
    definition = Column(Text, nullable=False, unique=False)
    """*Event's definition*  
        **str** : nullable=False, unique=False"""
    annotation = Column(String(16), nullable=False, unique=False)
    """*Event's annotation (displayed in old format dictionary HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""
    suffix = Column(String(16), nullable=False, unique=False)
    """*Event's suffix (used to create filename when exporting HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""

    _deprecated_words = relationship(
        "BaseWord", back_populates="_event_end",
        foreign_keys="BaseWord.event_end_id")

    _appeared_words = relationship(
        "BaseWord", back_populates="_event_start",
        foreign_keys="BaseWord.event_start_id")

    @property
    def deprecated_words(self):
        """
        *Relationship query for getting a list of words deprecated during this event*

        **query** : Optional[List[BaseWord]]"""

        return self._deprecated_words

    @property
    def appeared_words(self):
        """
        *Relationship query for getting a list of words appeared during this event*

        **query** : Optional[List[BaseWord]]"""

        return self._appeared_words

    @classmethod
    def latest(cls, session: Session) -> BaseEvent:
        """
        Gets the latest (current) `BaseEvent` from DB
        """
        return session.execute(select(cls).order_by(cls.id.desc())).scalars().first()
