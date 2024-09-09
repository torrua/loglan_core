"""
This module contains a basic Type Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, mapped_column, Mapped

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
        type_: Mapped[str_016],
        type_x: Mapped[str_016],
        group: Mapped[str_016],
        parentable: Mapped[bool],
        description: Mapped[str_255] | None = None,
    ):
        """
        Returns:
        """
        super().__init__()
        self.type_ = type_
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
            f"{self.type_} ({self.type_x})>"
        )

    type_: Mapped[str_016] = mapped_column("type", nullable=False)  # E.g. 2-Cpx, C-Prim
    type_x: Mapped[str_016] = mapped_column(nullable=False)  # E.g. Predicate, Predicate
    group: Mapped[str_016] = mapped_column(nullable=False)  # E.g. Cpx, Prim
    parentable: Mapped[bool] = mapped_column(nullable=False)  # E.g. True, False
    description: Mapped[str_255 | None]  # E.g. Two-term Complex, ...

    words: Mapped[list[BaseWord]] = relationship(
        back_populates="type",
    )
