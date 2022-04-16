# -*- coding: utf-8 -*-
# pylint: disable=C0303
"""
This module contains a basic Author Model
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from loglan_core.base import BaseModel
from loglan_core.connect_tables import t_connect_authors
from loglan_core.table_names import T_NAME_AUTHORS

__pdoc__ = {
    'BaseAuthor.created': False, 'BaseAuthor.updated': False,
}


class BaseAuthor(BaseModel):
    """Base Author's DB Model

    Describes a table structure for storing information about words authors.

    Connects with words with "many-to-many" relationship. See `t_connect_authors`.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 13, 'full_name': 'James Cooke Brown',
    'abbreviation': 'JCB', 'notes': ''}

    {'id': 29, 'full_name': 'Loglan 4&5',
    'abbreviation': 'L4',
    'notes': 'The printed-on-paper book,
              1975 version of the dictionary.'}
    ```
    </p></details>
    """

    __tablename__ = T_NAME_AUTHORS

    def __init__(self, abbreviation, full_name, notes):
        super().__init__()
        self.abbreviation = abbreviation
        self.full_name = full_name
        self.notes = notes

    abbreviation = Column(String(64), nullable=False, unique=True)
    """*Author's abbreviation (used in the LOD dictionary)*  
        **str** : max_length=64, nullable=False, unique=True
    Example:
        > JCB, L4
    """

    full_name = Column(String(64), nullable=True, unique=False)
    """
    *Author's full name (if exists)*  
        **str** : max_length=64, nullable=True, unique=False
    Example:
        > James Cooke Brown, Loglan 4&5
    """

    notes = Column(String(128), nullable=True, unique=False)
    """*Any additional information about author*  
        **str** : max_length=128, nullable=True, unique=False
    """

    _contribution = relationship(
        "BaseWord", back_populates="_authors", secondary=t_connect_authors)

    @property
    def contribution(self):
        """
        *Relationship query for getting a list of words coined by this author*
         **query** : Optional[List[BaseWord]]
        """
        return self._contribution
