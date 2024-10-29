"""
This module provides a base selector for SQLAlchemy
"""

from typing import Type, Iterable, Any

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, InstrumentedAttribute, joinedload
from sqlalchemy.types import String, Integer
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
            model (Type): The SQLAlchemy model class to select from.
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
            self._statement = self._statement.where(self.get_like_condition(key, value))
        return self

    def get_like_condition(self, key: str | InstrumentedAttribute, value: Any):
        """Generate the condition based on settings provided by Selector instance
        like (is_sqlite, case_sensitive).

        Args:
            key (str | InstrumentedAttribute): The key of the column to filter by.
            value (Any): The value to filter by.

        Returns:
            Condition: The SQLAlchemy condition to filter by.
        """
        column = self._get_column(key)

        if not isinstance(column.type, (String, Integer)):
            return column == value

        if isinstance(column.type, Integer):
            return column == int(value)

        value = value.replace("*", "%")

        if not self.case_sensitive:
            return column.ilike(value)

        if self.is_sqlite:
            return column.op("GLOB")(value)

        return column.like(value)

    def get_statement(self) -> Select:
        """Get the current SQLAlchemy _statement.

        Returns:
            Select: The current SQLAlchemy _statement.
        """
        return self._statement

    def with_relationships(self, selected: Iterable[str] | None = None) -> Self:
        """Adds relationships to the query.

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

    @staticmethod
    def _is_model_accepted(model, parent: type[BaseModel] = BaseModel):
        """Checks if the model is an instance of BaseModel or its child.

        Raises:
            ValueError: If the model is not an instance of BaseModel or its child.
        """
        if not issubclass(model, parent):
            raise ValueError(f"Provided model={model} is not a inherited from {parent}")

    def _get_column(self, key: str | InstrumentedAttribute) -> InstrumentedAttribute:
        """Get the column from the model.

        Args:
            key (str | InstrumentedAttribute): The key of the column to filter by.

        Raises:
            AttributeError: If the model has no attribute with the given key.

        Returns:
            InstrumentedAttribute: The SQLAlchemy column to filter by.
        """
        column = getattr(self.model, key, None) if isinstance(key, str) else key
        if column is None:
            raise AttributeError(f"Model {self.model} has no attribute {key}")
        return column

    def execute(self, session: Session, unique: bool = False) -> Any:
        """Executes the given session and returns the result.

        Args:
            session (Session): SQLAlchemy Session object.
            unique (bool, optional): Flag indicating if the result should be unique.
            Defaults to False.
        Returns:
            ResultProxy: The result of the executed session.
        """
        result = session.execute(self._statement)
        return result.unique() if unique else result

    def all(self, session: Session, unique: bool = False):
        """Executes the given session and returns all the results as a list.

        Args:
            session (Session): SQLAlchemy Session object.
            unique (bool, optional): Flag indicating if the result should contain unique items.
            Defaults to False.
        Returns:
            List[ResultRow]: All the results of the executed session.
        """
        return self.execute(session, unique).scalars().all()

    def scalar(self, session: Session):
        """Executes the given session and returns a scalar result.

        Args:
            session (Session): SQLAlchemy Session object.

        Returns:
            Any: The scalar result of the executed session.
        """
        return self.execute(session).scalar()

    def fetchmany(
        self, session: Session, size: int | None = None, unique: bool = False
    ):
        """Executes the given session and fetches a specified number of results.

        Args:
            session (Session): SQLAlchemy Session object.
            size (int, optional): Number of results to fetch. If None, fetches all results.
            unique (bool, optional): Flag indicating if the result should contain unique items.
            Defaults to False.
        Returns:
            List[ResultRow]: The fetched results.
        """
        return self.execute(session, unique).scalars().fetchmany(size)

    async def execute_async(self, session: AsyncSession, unique: bool = False):
        """Executes the given session and returns the result.

        Args:
            session (AsyncSession): SQLAlchemy Session object.
            unique (bool, optional): Flag indicating if the result should be unique.
            Defaults to False.
        Returns:
            ResultProxy: The result of the executed session.
        """
        result = await session.execute(self._statement)
        return result.unique() if unique else result

    async def all_async(self, session: AsyncSession, unique: bool = False):
        """Executes the given session and returns all the results as a list.

        Args:
            session (AsyncSession): SQLAlchemy Session object.
            unique (bool, optional): Flag indicating if the result should contain unique items.
            Defaults to False.
        Returns:
            List[ResultRow]: All the results of the executed session.
        """
        result = await self.execute_async(session, unique)
        return result.scalars().all()

    async def scalar_async(self, session: AsyncSession):
        """Executes the given session and returns a scalar result.

        Args:
            session (AsyncSession): SQLAlchemy Session object.

        Returns:
            Any: The scalar result of the executed session.
        """
        result = await self.execute_async(session)
        return result.scalar()

    async def fetchmany_async(
        self, session: AsyncSession, size: int | None = None, unique: bool = False
    ):
        """Executes the given session and fetches a specified number of results.

        Args:
            session (AsyncSession): SQLAlchemy Session object.
            size (int, optional): Number of results to fetch. If None, fetches all results.
            unique (bool, optional): Flag indicating if the result should contain unique items.
            Defaults to False.
        Returns:
            List[ResultRow]: The fetched results.
        """
        result = await self.execute_async(session, unique)
        return result.scalars().fetchmany(size)
