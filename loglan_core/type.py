# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic Type Model
"""
from typing import Union, List

from sqlalchemy import Column, String, Boolean
from sqlalchemy import or_, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from loglan_core.base import BaseModel
from loglan_core.table_names import T_NAME_TYPES

__pdoc__ = {
    'BaseType.words': 'words',
    'BaseType.created': False, 'BaseType.updated': False,
}


class BaseType(BaseModel):
    """BaseType model"""
    __tablename__ = T_NAME_TYPES

    def __init__(self, type, type_x, parentable, group, description):
        super().__init__()
        self.type = type
        self.type_x = type_x
        self.parentable = parentable
        self.group = group
        self.description = description

    type = Column(String(16), nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x = Column(String(16), nullable=False)  # E.g. Predicate, Predicate
    group = Column(String(16))  # E.g. Cpx, Prim
    parentable = Column(Boolean, nullable=False)  # E.g. True, False
    description = Column(String(255))  # E.g. Two-term Complex, ...

    _words = relationship(
        "BaseWord", back_populates="_type",
        foreign_keys="BaseWord.type_id")

    @property
    def words(self):
        """

        Returns:

        """
        return self._words

    @classmethod
    def by(cls, session: Session, type_filter: Union[str, List[str]]):
        """

        Args:
          session:
          type_filter: Union[str, List[str]]:

        Returns:

        """

        type_filter = [type_filter, ] if isinstance(type_filter, str) else type_filter
        type_request = select(cls).filter(or_(
            cls.type.in_(type_filter), cls.type_x.in_(type_filter), cls.group.in_(type_filter), ))
        return session.execute(type_request).scalars().all()
