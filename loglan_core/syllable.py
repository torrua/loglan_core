"""
This module contains a basic Syllable Model
"""

from sqlalchemy.orm import mapped_column, Mapped

from loglan_core.base import BaseModel
from loglan_core.base import str_008, str_032
from loglan_core.table_names import T_NAME_SYLLABLES

__pdoc__ = {
    "BaseSyllable.created": False,
    "BaseSyllable.updated": False,
}


class BaseSyllable(BaseModel):
    """Base Syllable's DB Model

    Describes a table structure for storing information about loglan syllables.

    <details><summary>Show Examples</summary><p>
    ```python
    {'id': 37, 'name': 'zv', 'type_': 'InitialCC', 'allowed': True}

    {'id': 38, 'name': 'cdz', 'type_': 'UnintelligibleCCC', 'allowed': False}
    ```
    </p></details>
    """

    __tablename__ = T_NAME_SYLLABLES

    def __init__(
        self,
        name: Mapped[str_008],
        type_: Mapped[str_032],
        allowed: Mapped[bool],
    ):
        super().__init__()
        self.name = name
        self.type_ = type_
        self.allowed = allowed

    def __str__(self):
        """
        Returns:
        """
        return (
            f"<{self.__class__.__name__}"
            f"{' ID ' + str(self.id) + ' ' if self.id else ' '}"
            f"{self.name} ({self.type_})>"
        )

    name: Mapped[str_008] = mapped_column(nullable=False)
    """*Syllable itself*  
            **str** : max_length=8, nullable=False, unique=False"""
    type_: Mapped[str_032] = mapped_column("type", nullable=False)
    """*Syllable's type*  
            **str** : max_length=8, nullable=False, unique=False"""
    allowed: Mapped[bool] = mapped_column(nullable=False)
    """*Is this syllable acceptable in grammar*  
            **bool** : nullable=False, unique=False"""
