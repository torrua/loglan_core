# -*- coding: utf-8 -*-
# pylint: disable=C0303

"""
This module contains a basic Event Model
"""
from __future__ import annotations

import datetime

from sqlalchemy import Text
from sqlalchemy import select, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.selectable import Select

from loglan_core.base import BaseModel, str_016, str_064
from loglan_core.table_names import T_NAME_EVENTS

__pdoc__ = {
    "BaseEvent.created": False,
    "BaseEvent.updated": False,
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

    def __init__(
        self,
        date: Mapped[datetime.date],
        name: Mapped[str_064],
        definition: Mapped[str],
        annotation: Mapped[str_016],
        suffix: Mapped[str_016],
    ):
        super().__init__()
        self.date = date
        self.name = name
        self.definition = definition
        self.annotation = annotation
        self.suffix = suffix

    date: Mapped[datetime.date] = mapped_column(nullable=False)
    """*Event's starting day*  
        **dateime.date** : nullable=False, unique=False"""
    name: Mapped[str_064] = mapped_column(nullable=False)
    """*Event's short name*  
        **str** : max_length=64, nullable=False, unique=False"""
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    """*Event's definition*
        **str** : nullable=False, unique=False"""
    annotation: Mapped[str_016] = mapped_column(nullable=False)
    """*Event's annotation (displayed in old format dictionary HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""
    suffix: Mapped[str_016] = mapped_column(nullable=False)
    """*Event's suffix (used to create filename when exporting HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""

    _deprecated_words: Mapped[list["BaseWord"]] = relationship(  # type: ignore
        "BaseWord",
        back_populates="_event_end",
        foreign_keys="BaseWord.event_end_id",
        lazy="dynamic",
    )

    _appeared_words: Mapped[list["BaseWord"]] = relationship(  # type: ignore
        "BaseWord",
        back_populates="_event_start",
        foreign_keys="BaseWord.event_start_id",
        lazy="dynamic",
    )

    @property
    def deprecated_words_query(self):
        """
        *Relationship query for getting a list of words deprecated during this event*

        **query** : Optional[List[BaseWord]]"""

        return self._deprecated_words

    @property
    def appeared_words_query(self):
        """
        *Relationship query for getting a list of words appeared during this event*

        **query** : Optional[List[BaseWord]]"""

        return self._appeared_words

    @property
    def deprecated_words(self) -> list["BaseWord"]:  # type: ignore
        """
        *Relationship query for getting a list of words deprecated during this event*

        **query** : Optional[List[BaseWord]]"""

        return self.deprecated_words_query.all()

    @property
    def appeared_words(self) -> list["BaseWord"]:  # type: ignore
        """
        *Relationship query for getting a list of words appeared during this event*

        **query** : Optional[List[BaseWord]]"""

        return self.appeared_words_query.all()

    @classmethod
    def latest(cls) -> Select:
        """
        Gets the latest (current) `BaseEvent` from DB
        """
        return select(cls).filter(cls.id == cls.latest_id())

    @classmethod
    def latest_id(cls):
        """
        Gets the id of the latest (current) `BaseEvent` from DB
        """
        return select(
            func.max(BaseEvent.id)  # pylint: disable=E1102
        ).scalar_subquery()
