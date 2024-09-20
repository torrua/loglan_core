"""
This module provides a base selector for SQLAlchemy
"""

from __future__ import annotations

from typing import Type, Iterable, Any

from sqlalchemy import select, Select
from sqlalchemy.orm import Session, InstrumentedAttribute, joinedload
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

    """

    def __init__(
        self,
        model: Type[BaseModel],
        is_sqlite: bool = False,
        case_sensitive: bool = False,
        disable_model_check: bool = False,
    ):
        """Initializes the Selector.

        Args:
            model (Type): The SQLAlchemy model class to query.
            is_sqlite (bool): Flag indicating if the database is SQLite.
            case_sensitive (bool): Flag indicating if the queries should be case-sensitive.
            disable_model_check (bool): Flag indicating if the model check should be disabled.
        """
        self.disable_model_check = disable_model_check
        if not self.disable_model_check:
            self._is_model_accepted(model, BaseModel)

        self.model = model
        self._statement = select(self.model)
        self._selected_columns = [self.model]

        self.is_sqlite = is_sqlite
        self.case_sensitive = case_sensitive

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
        return session.execute(self._statement).scalars().all()

    def scalar(self, session: Session):
        """
        Executes the given session and returns a scalar result.

        Args:
            session (Session): SQLAlchemy Session object.

        Returns:
            Any: The scalar result of the executed session.
        """
        return session.execute(self._statement).scalar()

    def fetchmany(self, session: Session, size: int | None = None):
        """
        Executes the given session and fetches a specified number of results.

        Args:
            session (Session): SQLAlchemy Session object.
            size (int, optional): Number of results to fetch. If None, fetches all results.

        Returns:
            List[ResultRow]: The fetched results.
        """
        return session.execute(self._statement).scalars().fetchmany(size)

    def select_columns(self, *columns: type[BaseModel]) -> Self:
        """Specify which columns to select without resetting the filters.

        Args:
            *columns: The columns to select.

        Returns:
            Self: The current instance for method chaining.
        """
        self._selected_columns = list(columns)
        existing_conditions = self._statement.whereclause

        if existing_conditions is None:
            self._statement = select(*self._selected_columns)
        else:
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

    def filter(self, *args) -> Self:
        """Filter results based on arbitrary keyword arguments.

        Args:
            *args: Column-value pairs to filter by.

        Returns:
            Self: The current instance for method chaining.
        """

        self._statement = self._statement.filter(*args)

        return self

    def filter_by(self, **kwargs) -> Self:
        """Filter results based on arbitrary keyword arguments.

        Args:
            *kwargs: Column-value pairs to filter by.

        Returns:
            Self: The current instance for method chaining.
        """

        self._statement = self._statement.filter_by(**kwargs)

        return self

    def where(self, *args) -> Self:
        """Filter results based on arbitrary keyword arguments.

        Args:
            *args: Column-value pairs to filter by.

        Returns:
            Self: The current instance for method chaining.
        """
        self._statement = self._statement.where(*args)
        return self

    def where_like(self, **kwargs) -> Self:
        """Filter results based on arbitrary keyword arguments.
            Use internal method `_generate_column_condition` to generate
            the condition based on settings provided by Selector instance
            like (is_sqlite, case_sensitive).

        Args:
            **kwargs: Column-value pairs to filter by.

        Returns:
            Self: The current instance for method chaining.
        """
        for key, value in kwargs.items():
            self._statement = self._statement.where(
                self._generate_column_condition(key, value)
            )
        return self

    def _generate_column_condition(self, key: str | InstrumentedAttribute, value: Any):
        column = getattr(self.model, key, None) if isinstance(key, str) else key
        if column is None:
            raise AttributeError(f"Model {self.model} has no attribute {key}")

        value = str(value).replace("*", "%")
        if self.case_sensitive:
            return column.op("GLOB")(value) if self.is_sqlite else column.like(value)
        return column.ilike(value)

    def get_statement(self) -> Select:
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
        return self.all(session)

    @staticmethod
    def _is_model_accepted(model, parent: type[BaseModel] = BaseModel):
        """
        Checks if the model is an instance of BaseModel or its child.
        Raises:
            ValueError: If the model is not an instance of BaseModel or its child.
        """
        if not issubclass(model, parent):
            raise ValueError(
                f"Provided class_={model} is not a inherited from {parent}"
            )

    def with_relationships(self, selected: Iterable[str] | None = None) -> Self:
        """
        Adds relationships to the query.

        Args:
            selected (set[str]): A set of relationship names to include.
            Defaults to None if all relationships should be included.

        Returns:
            Self: A query with the relationships added.
        """
        available_relationships = {
            attr: getattr(self.model, attr) for attr in self.model.relationships()
        }
        relationships = {
            joinedload(v)
            for k, v in available_relationships.items()
            if not selected or k in selected
        }
        self._statement = self._statement.options(*relationships)
        return self
