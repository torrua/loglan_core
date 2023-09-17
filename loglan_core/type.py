# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
This module contains a basic Type Model
"""
from sqlalchemy import or_, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.orm.session import Session

from loglan_core.base import BaseModel
from loglan_core.base import str_016, str_255
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

    type: Mapped[str_016] = mapped_column(nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x: Mapped[str_016] = mapped_column(nullable=False)  # E.g. Predicate, Predicate
    group: Mapped[str_016 | None]  # E.g. Cpx, Prim
    parentable: Mapped[bool] = mapped_column(nullable=False)  # E.g. True, False
    description: Mapped[str_255 | None]  # E.g. Two-term Complex, ...

    _words: Mapped[list["BaseWord"]] = relationship(back_populates="_type",
        foreign_keys="BaseWord.type_id")

    @property
    def words(self):
        """

        Returns:

        """
        return self._words

    @classmethod
    def by(cls, session: Session, type_filter: str| list[str]):
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
