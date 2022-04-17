# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic Word Model
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Date, JSON
from sqlalchemy import select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.session import Session

from loglan_core.author import BaseAuthor
from loglan_core.base import BaseModel
from loglan_core.connect_tables import t_connect_authors, t_connect_words, t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey
from loglan_core.table_names import T_NAME_EVENTS, T_NAME_TYPES, T_NAME_WORDS
from loglan_core.type import BaseType

__pdoc__ = {
    'BaseWord.created': False, 'BaseWord.updated': False,
}


class BaseWord(BaseModel):
    """BaseWord model"""
    __tablename__ = T_NAME_WORDS

    def __init__(
            self, id_old: int, name: str, type_id: int,
            event_start_id: int, event_end_id: int = None, tid_old: int = None,
            origin: str = None, origin_x: str = None, match: str = None,
            rank: str = None, year: datetime.date = None, notes: dict = None, ):

        super().__init__()

        self.id_old = id_old
        self.name = name
        self.type_id = type_id
        self.event_start_id = event_start_id

        self.event_end_id = event_end_id
        self.tid_old = tid_old

        self.origin = origin
        self.origin_x = origin_x
        self.match = match
        self.rank = rank
        self.year = year

        self.notes = notes

    def __repr__(self):
        return f"<{self.__class__.__name__}" \
               f"{' ID ' + str(self.id) + ' ' if self.id else ' '}" \
               f"'{self.name}'>"

    id = Column(Integer, primary_key=True)
    """Word's internal ID number: Integer"""

    name = Column(String(64), nullable=False)
    origin = Column(String(128))
    origin_x = Column(String(64))
    match = Column(String(8))
    rank = Column(String(8))
    year = Column("year", Date)
    notes = Column("notes", JSON)

    # Field for legacy database compatibility
    id_old = Column(Integer, nullable=False)
    tid_old = Column("TID_old", Integer)  # references

    # Relationships
    type_id = Column("type", ForeignKey(f'{T_NAME_TYPES}.id'), nullable=False)

    _type = relationship(
        BaseType.__name__, back_populates="_words")

    @property
    def type(self) -> BaseType:
        return self._type

    event_start_id = Column(
        "event_start", ForeignKey(f'{T_NAME_EVENTS}.id'), nullable=False)

    _event_start = relationship(
        BaseEvent.__name__, foreign_keys=[event_start_id],
        back_populates="_appeared_words")

    @property
    def event_start(self) -> BaseEvent:
        """

        Returns:

        """
        return self._event_start

    event_end_id = Column("event_end", ForeignKey(f'{T_NAME_EVENTS}.id'))

    _event_end = relationship(
        BaseEvent.__name__, foreign_keys=[event_end_id],
        back_populates="_deprecated_words")

    @property
    def event_end(self) -> BaseEvent:
        """

        Returns:

        """
        return self._event_end

    _authors = relationship(
        BaseAuthor.__name__, secondary=t_connect_authors,
        back_populates="_contribution", lazy='dynamic', enable_typechecks=False)

    @property
    def authors_query(self):
        return self._authors

    @property
    def authors(self) -> list[BaseAuthor]:
        """

        Returns:

        """
        return self._authors.all()

    _definitions = relationship(
        BaseDefinition.__name__, back_populates="_source_word", lazy='dynamic')

    @property
    def definitions_query(self):
        return self._definitions

    @property
    def definitions(self) -> list[BaseDefinition]:
        """

        Returns:

        """
        return self.definitions_query.order_by(BaseDefinition.position.asc()).all()

    # word's derivatives
    _derivatives = relationship(
        'BaseWord', secondary=t_connect_words,
        primaryjoin=(t_connect_words.c.parent_id == id),
        secondaryjoin=(t_connect_words.c.child_id == id),
        backref=backref('_parents', lazy='dynamic', enable_typechecks=False),
        lazy='dynamic', enable_typechecks=False)

    @property
    def derivatives_query(self):
        return self._derivatives

    @property
    def derivatives(self):
        return self.derivatives_query.all()

    def derivatives_query_by(
            self, word_type: str = None, word_type_x: str = None,
            word_group: str = None, type_class=BaseType):
        """Query to get all derivatives of the word, depending on its parameters

        Args:
          word_type: str:  (Default value = None)
          E.g. "2-Cpx", "C-Prim", "LW"<hr>

          word_type_x: str:  (Default value = None)
          E.g. "Predicate", "Name", "Affix"<hr>

          word_group: str:  (Default value = None)
          E.g. "Cpx", "Prim", "Little"<hr>

          type_class:
        Returns:
            List[Word]
        """

        type_values = [
            (type_class.type, word_type),
            (type_class.type_x, word_type_x),
            (type_class.group, word_group), ]

        type_filters = [i[0] == i[1] for i in type_values if i[1]]

        return self.derivatives_query.join(type_class)\
            .filter(self.id == t_connect_words.c.parent_id, *type_filters)\
            .order_by(type(self).name.asc())

    @property
    def affixes(self):
        """
        Get all word's affixes if exist
        Only primitives have affixes.

        Returns:
            BaseQuery
        """
        return self.derivatives_query_by(word_type="Afx").all()

    @property
    def complexes(self):
        """
        Get all word's complexes if exist
        Only primitives and Little Words have complexes.

        Returns:
            BaseQuery
        """
        return self.derivatives_query_by(word_group="Cpx").all()

    @property
    def parents_query(self):
        """Query to get all parents for Complexes, Little words or Affixes

        Returns:
            BaseQuery
        """
        return self._parents

    @property
    def parents(self):
        return self.parents_query.all()

    @property
    def keys_query(self):
        """Get all BaseKey object related to this BaseWord.

        Keep in mind that duplicated keys from related definitions
        will be counted with ```.count()``` but excluded from ```.all()``` request

        Returns:
        """
        return select(BaseKey).\
            join(t_connect_keys).\
            join(BaseDefinition, BaseDefinition.id == t_connect_keys.c.DID).\
            join(BaseWord, BaseWord.id == BaseDefinition.word_id).\
            filter(BaseWord.id == self.id).order_by(BaseKey.word.asc())

    def keys(self, session: Session) -> list:
        return session.execute(self.keys_query).scalars().all()
