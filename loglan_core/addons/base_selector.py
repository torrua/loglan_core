"""
This module provides a base selector for SQLAlchemy
"""

from __future__ import annotations

from typing import Any, Type

from sqlalchemy import Select, BinaryExpression
from sqlalchemy.orm import Session, InstrumentedAttribute

from loglan_core.base import BaseModel


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

    condition_by_attribute(
        class_: Type[BaseModel],
        attr: InstrumentedAttribute | str,
        value: Any,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        use_wildcard: bool = True,
        wildcard_symbol: str = "*",
    ) -> BinaryExpression:
        Creates a filter to select items by a specific attribute value.
        Support wildcard and case-sensitive search.
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

    @classmethod
    def condition_by_attribute(
        cls,
        class_: Type[BaseModel],
        attr: InstrumentedAttribute | str,
        value: Any,
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        use_wildcard: bool = True,
        wildcard_symbol: str = "*",
    ) -> BinaryExpression:
        """
        Applies a filter to select words by a specific attribute value.

        Args:
            class_ (BaseModel): The class to select from.
            attr (str): The attribute to filter by.
            value (Any): The value of the attribute to filter by.
            is_sqlite (bool): If SQLite is being used. Defaults to False.
            case_sensitive (bool): Whether the search should be case-sensitive.
                Defaults to False.
            use_wildcard (bool): Whether to use wildcards. Defaults to True.
            wildcard_symbol (str): The symbol to use for wildcards. Defaults to "*".

        Returns:
            BaseSelector: A query with the filter applied.
        """

        cls._is_class_acceptable(class_)
        attr = cls._get_attr(class_, attr)

        if use_wildcard:
            value = str(value).replace(wildcard_symbol, "%")

        if case_sensitive:
            return attr.op("GLOB")(value) if is_sqlite else attr.like(value)
        return attr.ilike(value)

    @staticmethod
    def _get_attr(
        class_: Type[BaseModel],
        attr: InstrumentedAttribute | str,
    ) -> InstrumentedAttribute:
        """
        Gets the attribute from the class.

        Args:
            class_ (BaseModel): The class to get the attribute from.
            attr (str | InstrumentedAttribute): The attribute to get.

        Raises:
            AttributeError: If the attribute is not found in the class.

        Returns:
            InstrumentedAttribute: The attribute from the class.
        """
        if isinstance(attr, str):
            try:
                return getattr(class_, attr)
            except AttributeError as exc:
                raise AttributeError(
                    f"Provided attribute={attr} is not an attribute of {class_}"
                ) from exc
        return attr

    @staticmethod
    def _is_class_acceptable(class_: Type[BaseModel]):
        """
        Checks if the class is an instance of BaseModel or its child.

        Args:
            class_ (Type[BaseModel]): The class to check.

        Raises:
            ValueError: If the class is not an instance of BaseModel or its child.
        """
        if not issubclass(class_, BaseModel):
            raise ValueError(
                f"Provided class_={class_} is not a {BaseModel} or its child"
            )
