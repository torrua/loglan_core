"""
This module contains a basic Event Model
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel, str_016, str_064
from loglan_core.table_names import T_NAME_EVENTS

if TYPE_CHECKING:
    from loglan_core.word import BaseWord

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
        event_id: Mapped[int],
        name: Mapped[str_064],
        date: Mapped[datetime.date],
        definition: Mapped[str],
        annotation: Mapped[str_016],
        suffix: Mapped[str_016],
    ):
        super().__init__()
        self.event_id = event_id
        self.name = name
        self.date = date
        self.definition = definition
        self.annotation = annotation
        self.suffix = suffix

    def __str__(self):
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.event_id) + ' ' if self.event_id else ' '}"
            f"{self.name} ({self.date})>"
        )

    event_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    """*Event's id*
        **int** : nullable=False, unique=True"""
    name: Mapped[str_064] = mapped_column(nullable=False)
    """*Event's short name*  
        **str** : max_length=64, nullable=False, unique=False"""
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    """*Event's starting day*  
        **dateime.date** : nullable=False, unique=False"""
    definition: Mapped[str] = mapped_column(Text, nullable=False)
    """*Event's definition*
        **str** : nullable=False, unique=False"""
    annotation: Mapped[str_016] = mapped_column(nullable=False)
    """*Event's annotation (displayed in old format dictionary HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""
    suffix: Mapped[str_016] = mapped_column(nullable=False)
    """*Event's suffix (used to create filename when exporting HTML file)*  
        **str** : max_length=16, nullable=False, unique=False"""

    deprecated_words: Mapped[list[BaseWord]] = relationship(
        "BaseWord",
        back_populates="event_end",
        foreign_keys="BaseWord.event_end_id",
    )

    appeared_words: Mapped[list[BaseWord]] = relationship(
        "BaseWord",
        back_populates="event_start",
        foreign_keys="BaseWord.event_start_id",
    )
