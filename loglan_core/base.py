# -*- coding: utf-8 -*-

"""
Initial common functions for LOD Model Classes
"""
from datetime import datetime
from typing import Set

from sqlalchemy import Column, TIMESTAMP, func, Integer
from sqlalchemy.orm import declarative_base, Session
Base = declarative_base()


class BaseModel(Base):
    """
    Init class for common methods
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated = Column(TIMESTAMP, onupdate=func.now())

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
            k: v for k, v in sorted(self.__dict__.items())
            if not str(k).startswith("_") and k not in ["created", "updated"]}

    @classmethod
    def attributes_all(cls) -> Set[str]:
        """

        Returns:

        """
        return set(cls.__mapper__.attrs.keys())

    @classmethod
    def attributes_basic(cls) -> Set[str]:
        """

        Returns:

        """
        return set(cls.attributes_all() - cls.relationships())

    @classmethod
    def attributes_extended(cls) -> Set[str]:
        """

        Returns:

        """
        return set(cls.attributes_all() - cls.foreign_keys())

    @classmethod
    def relationships(cls) -> Set[str]:
        """

        Returns:

        """
        return set(cls.__mapper__.relationships.keys())

    @classmethod
    def foreign_keys(cls) -> Set[str]:
        """

        Returns:

        """
        return set(cls.attributes_all() - cls.relationships() - cls.non_foreign_keys())

    @classmethod
    def non_foreign_keys(cls) -> Set[str]:
        """

        Returns:

        """
        return {column.name for column in cls.__table__.columns if not column.foreign_keys}
