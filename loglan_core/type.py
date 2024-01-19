"""
This module contains a basic Type Model
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import or_, select
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.selectable import Select

from loglan_core.base import BaseModel
from loglan_core.base import str_016, str_255
from loglan_core.table_names import T_NAME_TYPES

if TYPE_CHECKING:
    from loglan_core.word import BaseWord

__pdoc__ = {
    "BaseType.words": "words",
    "BaseType.created": False,
    "BaseType.updated": False,
}


class BaseType(BaseModel):
    """BaseType model"""

    __tablename__ = T_NAME_TYPES

    def __init__(
            self,
            type: Mapped[str_016],  # pylint: disable=W0622
            type_x: Mapped[str_016],
            group: Mapped[str_016],
            parentable: Mapped[bool],
            description: Mapped[str_255] | None = None,
    ):
        """
        Returns:
        """
        super().__init__()
        self.type = type
        self.type_x = type_x
        self.group = group
        self.parentable = parentable
        self.description = description

    def __str__(self):
        """
        Returns:
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.type} ({self.type_x})>"
        )

    type: Mapped[str_016] = mapped_column(nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x: Mapped[str_016] = mapped_column(nullable=False)  # E.g. Predicate, Predicate
    group: Mapped[str_016] = mapped_column(nullable=False)  # E.g. Cpx, Prim
    parentable: Mapped[bool] = mapped_column(nullable=False)  # E.g. True, False
    description: Mapped[str_255 | None]  # E.g. Two-term Complex, ...

    relationship_words: Mapped[list[BaseWord]] = relationship(  # type: ignore
        back_populates="relationship_type",
        foreign_keys="BaseWord.type_id",
        lazy="dynamic",
    )

    @property
    def words_query(self):
        """
        Returns:
        """
        return self.relationship_words

    @property
    def words(self) -> list[BaseWord]:
        """
        Returns:
        """
        return self.words_query.all()

    @classmethod
    def by_property(cls, type_filter: str | list[str], id_only: bool = False) -> Select:
        """
        Args:
          type_filter: Union[str, List[str]]:
          id_only: bool:
        Returns:
        """

        type_filter = (
            [
                type_filter,
            ]
            if isinstance(type_filter, str)
            else type_filter
        )

        type_request = select(cls.id if id_only else cls).filter(
            or_(
                cls.type.in_(type_filter),
                cls.type_x.in_(type_filter),
                cls.group.in_(type_filter),
            )
        )
        return type_request
