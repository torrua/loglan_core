# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""
Initial common functions for LOD Model Classes
"""
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import registry as rg
from typing_extensions import Annotated

str_008 = Annotated[str, 8]
str_016 = Annotated[str, 16]
str_032 = Annotated[str, 32]
str_064 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_255 = Annotated[str, 255]


class BaseModel(DeclarativeBase):
    """Declarative Base Model"""

    registry = rg(
        type_annotation_map={
            str_008: String(8),
            str_016: String(16),
            str_032: String(32),
            str_064: String(64),
            str_128: String(128),
            str_255: String(255),
        }
    )

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated: Mapped[datetime | None] = mapped_column(
        onupdate=func.now()  # pylint: disable=E1102
    )

    def __repr__(self):
        obj_str = ", ".join(
            sorted(
                [
                    f"{k}={v!r}"
                    for k, v in self.__dict__.items()
                    if not k.startswith("_") and k not in ["created", "updated"]
                ]
            )
        )
        return f"{self.__class__.__name__}({obj_str})"

    @classmethod
    def get_by_id(cls, session: Session, cid: int):
        """
        Get model object from DB by its id
        :param session: session
        :param cid: cls id
        :return:
        """
        return session.query(cls).filter(cls.id == cid).first()

    @classmethod
    def get_all(cls, session: Session):
        """
        Get all model objects from DB
        :param session: session
        :return:
        """
        return session.query(cls).all()

    def export(self):
        """
        Export record data from DB
        Should be redefined in model's class
        Returns:
        """
        return {
            k: v
            for k, v in sorted(self.__dict__.items())
            if not str(k).startswith("_") and k not in ["created", "updated"]
        }

    @classmethod
    def attributes_all(cls) -> set[str]:
        """
        Returns:
        """
        return set(cls.__mapper__.attrs.keys())

    @classmethod
    def attributes_basic(cls) -> set[str]:
        """
        Returns:
        """
        return set(cls.attributes_all() - cls.relationships())

    @classmethod
    def attributes_extended(cls) -> set[str]:
        """
        Returns:
        """
        return set(cls.attributes_all() - cls.foreign_keys())

    @classmethod
    def relationships(cls) -> set[str]:
        """
        Returns:
        """
        return set(cls.__mapper__.relationships.keys())

    @classmethod
    def foreign_keys(cls) -> set[str]:
        """
        Returns:
        """
        return set(cls.attributes_all() - cls.relationships() - cls.non_foreign_keys())

    @classmethod
    def non_foreign_keys(cls) -> set[str]:
        """
        Returns:
        """
        return {
            column.name for column in cls.__table__.columns if not column.foreign_keys
        }
