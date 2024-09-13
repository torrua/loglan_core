# pylint: disable=invalid-name
"""
Initial common functions for LOD Model Classes
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, inspect, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session, registry as rg
from typing_extensions import Annotated

str_008 = Annotated[str, 8]
"""
A custom type annotation that annotates a string with a metadata value 
of 8. It can be used to associate a string with the number 8 in certain 
contexts, such as specifying the length for a string field in a database.
"""

str_016 = Annotated[str, 16]
"""
A custom type annotation that annotates a string with a metadata value 
of 16. It can be used to associate a string with the number 16 in certain 
contexts, such as specifying the length for a string field in a database.
"""

str_032 = Annotated[str, 32]
"""
A custom type annotation that annotates a string with a metadata value 
of 32. It can be used to associate a string with the number 32 in certain 
contexts, such as specifying the length for a string field in a database.
"""

str_064 = Annotated[str, 64]
"""
A custom type annotation that annotates a string with a metadata value 
of 64. It can be used to associate a string with the number 64 in certain 
contexts, such as specifying the length for a string field in a database.
"""

str_128 = Annotated[str, 128]
"""
A custom type annotation that annotates a string with a metadata value 
of 128. It can be used to associate a string with the number 128 in certain 
contexts, such as specifying the length for a string field in a database.
"""

str_255 = Annotated[str, 255]
"""
A custom type annotation that annotates a string with a metadata value 
of 255. It can be used to associate a string with the number 255 in certain 
contexts, such as specifying the length for a string field in a database.
"""


class BaseModel(DeclarativeBase):
    """
    BaseModel is a subclass of DeclarativeBase. It serves as the parent class
    for other database models, providing common attributes and methods to its
    child classes. It doesn't contain any class-specific attributes/methods.
    """

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
    """
    This code creates a registry that maps custom type annotations to 
    SQLAlchemy String types with specified lengths. The keys are custom 
    type annotation names and the values are SQLAlchemy String types with 
    the specified lengths.
    """

    __abstract__ = True
    """
    A class attribute that indicates that this class is an abstract base 
    class. When set to True, this class won't be mapped to any database 
    table. Instead, it serves as a base for other classes which will be 
    mapped to tables.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    """
    A class attribute mapped to a column in the database table. It serves as 
    the primary key for the table.
 
    :type: int
    """

    created: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    """
    A class attribute mapped to a column in the database table. It represents 
    the timestamp when a row is created. The default value is the current 
    timestamp, and it can't be null.
    
    :type: datetime
    """

    updated: Mapped[datetime | None] = mapped_column(
        onupdate=func.now()  # pylint: disable=E1102
    )
    """
    A class attribute mapped to a column in the database table. It represents 
    the timestamp when a row is last updated. Whenever the row is updated, 
    this timestamp is automatically set to the current time. It can be ``null`` 
    if the row has never been updated.
    
    :type: datetime
    """

    def __repr__(self):
        """
        Special method that returns a string representation of the object.
        It forms the string by joining key-value pairs of the object's attributes,
        excluding keys that start with "_" and keys that are "created" or "updated".
        The key-value pairs are sorted before joining.

        Returns:
            str: A string representation of the object in the format:
                 "ClassName(key1=value1, key2=value2, ...)".
        """
        obj_str = ", ".join(
            sorted(
                [
                    f"{k}={v!r}"
                    for k, v in self.__dict__.items()
                    if self._filter_add_to_repr(k, v)
                ]
            )
        )
        return f"{self.__class__.__name__}({obj_str})"

    @classmethod
    def _filter_add_to_repr(cls, k, v):
        """
        Static method that filters out keys that start with "_" and keys
        that are "created" or "updated" and keys without values from the
        object's attributes. The method is used to generate a string
        representation of the object. It is used internally by the __repr__.
        """
        return (
            not k.startswith("_")
            and k not in ["created", "updated", *cls.relationships()]
            and v
        )

    @classmethod
    def get_by_id(cls, session: Session, cid: int):
        """
        Class method that retrieves an instance of the class from the
        database using the provided session and id.

        Parameters:
            session (Session): The session to use for the database query.
            cid (int): The id of the instance to retrieve.

        Returns:
            Object of class type or None: The instance of the class with
            the given id, or None if no such instance exists.
        """
        return session.get(cls, cid)

    @classmethod
    def get_all(cls, session: Session):
        """
        Class method that retrieves all instances of the class from the
        database using the provided session.

        Parameters:
            session (Session): The session to use for the database query.

        Returns:
            list: A list of all instances of the class.
        """
        return session.scalars(select(cls)).all()

    def export(self):
        """
        Class method that exports the object's attributes into a dictionary.
        It filters out keys that start with "_" and keys that are
        "created" or "updated", then sorts the remaining keys.

        Returns:
            dict: A dictionary with sorted keys and corresponding
            values of the object's attributes.
        """
        return {
            k: v
            for k, v in sorted(self.__dict__.items())
            if not str(k).startswith("_")
            and k not in ["created", "updated", *self.relationships()]
        }

    @classmethod
    def attributes_all(cls) -> set[str]:
        """
        Class method that computes the all attribute keys from the class
        mapper and returns their names as a set.

        It doesn't require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of all attribute keys.
        """
        return set(cls.__mapper__.attrs.keys()) | cls.hybrid_properties()

    @classmethod
    def attributes_basic(cls) -> set[str]:
        """
        Class method that computes the set of basic attributes for the class.
        It subtracts any relationships from all attributes.

        It doesn’t require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of basic attributes.
        """
        return set(cls.attributes_all() - cls.relationships() - cls.hybrid_properties())

    @classmethod
    def attributes_extended(cls) -> set[str]:
        """
        Class method that computes the extended attributes of the class.
        It does this by subtracting foreign keys from all attributes.

        It doesn’t require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of the extended attributes.
        """
        return set(cls.attributes_all() - cls.foreign_keys())

    @classmethod
    def relationships(cls) -> set[str]:
        """
        Class method that computes the relationship names from the
        class mapper and returns them as a set.

        It doesn't require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of the relationships.
        """
        return set(cls.__mapper__.relationships.keys())

    @classmethod
    def foreign_keys(cls) -> set[str]:
        """
        Class method that computes the names of foreign keys of the class.
        It does this by subtracting relationship keys and non-foreign keys
        from all attributes.

        It doesn’t require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of the foreign keys.
        """
        return set(
            cls.attributes_all()
            - cls.relationships()
            - cls.non_foreign_keys()
            - cls.hybrid_properties()
        )

    @classmethod
    def non_foreign_keys(cls) -> set[str]:
        """
        Class method that computes the non-foreign keys of the class.
        It does this by inspecting the class columns and selecting those
        without foreign keys.

        It doesn’t require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of the non-foreign keys.
        """
        inspector = inspect(cls)
        columns = inspector.columns
        non_foreign_keys = {
            column.name for column in columns if not column.foreign_keys
        }
        return non_foreign_keys

    @classmethod
    def hybrid_properties(cls) -> set[str]:
        """
        Class method that computes the hybrid properties of the class.

        It doesn’t require any parameters as it operates on the class itself.

        Returns:
            set[str]: A set of strings with names of the hybrid properties.
        """
        inspector = inspect(cls).all_orm_descriptors
        return {i.__name__ for i in inspector if isinstance(i, hybrid_property)}
