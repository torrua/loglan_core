"""
This module contains a basic Type Model
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import BaseModel
from .service.annotated_types import str_016, str_255
from .service.table_names import T_NAME_TYPES

if TYPE_CHECKING:
    from .word import BaseWord


class BaseType(BaseModel):
    """BaseType model"""

    __tablename__ = T_NAME_TYPES

    def __init__(  # pylint: disable=too-many-positional-arguments
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
