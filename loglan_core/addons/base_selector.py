"""
This module provides a base selector for SQLAlchemy
"""

from __future__ import annotations

from typing import Type

from sqlalchemy import true, and_, select
from sqlalchemy.orm import Session
from typing_extensions import Self

from loglan_core.base import BaseModel


class BaseSelector:  # pylint: disable=too-many-ancestors
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
        return session.execute(self._statement)

    def all(self, session: Session):
        """
        Executes the given session and returns all the results as a list.

        Args:
        session (Session): SQLAlchemy Session object.

        Returns:
        List[ResultRow]: All the results of the executed session.
        """
        return session.scalars(self._statement).all()

    def scalar(self, session: Session):
        """
        Executes the given session and returns a scalar result.

        Args:
        session (Session): SQLAlchemy Session object.

        Returns:
        Any: The scalar result of the executed session.
        """
        return session.scalar(self._statement)

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

    def __init__(
        self,
        model: Type[BaseModel],
        is_sqlite: bool = False,
        case_sensitive: bool = False,
    ):
        """Initializes the WordSelector.

        Args:
            model (Type): The SQLAlchemy model class to query.
            is_sqlite (bool): Flag indicating if the database is SQLite.
            case_sensitive (bool): Flag indicating if the queries should be case-sensitive.
        """

        self._is_model_accepted(model)
        self.model = model

        self.is_sqlite = is_sqlite
        self.case_sensitive = case_sensitive

        self._statement = select(self.model)
        self._selected_columns = [self.model]

    def select_columns(self, *columns) -> Self:
        """Specify which columns to select without resetting the filters.

        Args:
            *columns: The columns to select.

        Returns:
            Self: The current instance for method chaining.
        """
        self._selected_columns = columns
        existing_conditions = self._statement._whereclause
        self._statement = select(*self._selected_columns).where(existing_conditions)
        return self

    def limit(self, limit: int) -> Self:
        """Limit the number of results returned.

        Args:
            limit (int): The maximum number of results to return.

        Returns:
            Self: The current instance for method chaining.
        """
        self._statement = self._statement.limit(limit)
        return self

    def offset(self, offset: int) -> Self:
        """Set the offset for the results returned.

        Args:
            offset (int): The number of results to skip before starting to return results.

        Returns:
            Self: The current instance for method chaining.
        """
        self._statement = self._statement.offset(offset)
        return self

    def order_by(self, *columns) -> Self:
        """Specify the order in which results should be returned.

        Args:
            *columns: The columns to order by.

        Returns:
            Self: The current instance for method chaining.
        """
        self._statement = self._statement.order_by(*columns)
        return self

    def filter_by(self, **kwargs) -> Self:
        """Filter results based on arbitrary keyword arguments.

        Args:
            **kwargs: Column-value pairs to filter by.

        Returns:
            Self: The current instance for method chaining.
        """
        for key, value in kwargs.items():
            condition = self._generate_column_condition(key, value)
            self._statement = self._statement.where(condition)

        return self

    def _generate_column_condition(self, key, value):
        column = getattr(self.model, key, None)
        if column is None:
            return true()

        value = str(value).replace("*", "%")
        if self.case_sensitive:
            return column.op("GLOB")(value) if self.is_sqlite else column.like(value)
        return column.ilike(value)

    def get_statement(self):
        """Get the current SQLAlchemy _statement.

        Returns:
            Select: The current SQLAlchemy _statement.
        """
        return self._statement

    def __call__(self, session: Session):
        """Execute the current _statement and return the results.

        Args:
            session (Session): The SQLAlchemy session to use for executing the query.

        Returns:
            list: The results of the query.
        """
        try:
            with session() as s:
                results = s.execute(self._statement).scalars().all()
            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def _is_model_accepted(model):
        """
        Checks if the model is an instance of BaseModel or its child.
        Raises:
            ValueError: If the model is not an instance of BaseModel or its child.
        """
        if not issubclass(model, BaseModel):
            raise ValueError(
                f"Provided class_={model} is not a inherited from {BaseModel}"
            )

    def where(self, *conditions) -> Self:
        """Add additional conditions to the current statement.

        Args:
            *conditions: One or more SQLAlchemy expressions to filter by.

        Returns:
            Self: The current instance for method chaining.
        """
        if not conditions:
            return self

        # Combine existing conditions with new ones
        existing_conditions = self._statement._whereclause
        if existing_conditions is None:
            self._statement = self._statement.where(and_(*conditions))
        else:
            self._statement = self._statement.where(
                and_(existing_conditions, *conditions)
            )

        return self
