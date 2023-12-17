"""
This module provides a base selector for SQLAlchemy
"""

from __future__ import annotations

from sqlalchemy import Select
from sqlalchemy.orm import Session


class BaseSelector(Select):  # pylint: disable=too-many-ancestors
    """
    A custom base selector that inherits from SQLAlchemy's Select class.
    This class provides methods to execute a session and fetch results
    in different ways. It also provides a way to fetch many results.

    Methods:
    --------
    execute(session: Session) -> ResultProxy:
        Executes the session and returns the result.

    all(session: Session) -> List[ResultRow]:
        Executes the session and returns all the results.

    scalar(session: Session) -> Any:
        Executes the session and returns a scalar result.

    fetchmany(session: Session, size: int | None = None) -> List[ResultRow]:
        Executes the session and fetches a specified number of results.
    """

    def execute(self, session: Session):
        """
        Executes the given session and returns the result.

        Args:
        session (Session): SQLAlchemy Session object.

        Returns:
        ResultProxy: The result of the executed session.
        """
        return session.execute(self)

    def all(self, session: Session):
        """
        Executes the given session and returns all the results as a list.

        Args:
        session (Session): SQLAlchemy Session object.

        Returns:
        List[ResultRow]: All the results of the executed session.
        """
        return self.execute(session).scalars().all()

    def scalar(self, session: Session):
        """
        Executes the given session and returns a scalar result.

        Args:
        session (Session): SQLAlchemy Session object.

        Returns:
        Any: The scalar result of the executed session.
        """
        return self.execute(session).scalar()

    def fetchmany(self, session: Session, size: int | None = None):
        """
        Executes the given session and fetches a specified number of results.

        Args:
        session (Session): SQLAlchemy Session object.
        size (int, optional): Number of results to fetch. If None, fetches all results.

        Returns:
        List[ResultRow]: The fetched results.
        """
        return self.execute(session).scalars().fetchmany(size)
