# -*- coding: utf-8 -*-
"""
This module contains an "Export extensions" for LOD dictionary SQL model.
Add export() function to db object for returning its text string presentation.
"""

from loglan_core.author import BaseAuthor
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.setting import BaseSetting
from loglan_core.syllable import BaseSyllable
from loglan_core.type import BaseType
from loglan_core.word import BaseWord
from loglan_core.word_spell import BaseWordSpell


class Exporter:
    """
    This class serves as a general exporter for various types of objects. The types of objects
    that can be exported include: BaseAuthor, BaseDefinition, BaseEvent, BaseSetting,
    BaseSyllable, BaseType, BaseWord, and BaseWordSpell. For each of these types of objects,
    there's an associated method that takes the object as an input and returns a formatted
    string suitable for export.

    Methods:
        export: The main method that uses a dictionary to map the type of the input object
                to the respective export method.
        export_author: Converts a BaseAuthor object to a formatted string.
        export_definition: Converts a BaseDefinition object to a formatted string.
        export_event: Converts a BaseEvent object to a formatted string.
        export_setting: Converts a BaseSetting object to a formatted string.
        export_syllable: Converts a BaseSyllable object to a formatted string.
        export_type: Converts a BaseType object to a formatted string.
        export_word: Converts a BaseWord object to a formatted string.
        export_word_spell: Converts a BaseWordSpell object to a formatted string.

    Raises:
        ValueError: If the object type is not supported for export.
    """

    @classmethod
    def export(cls, obj):
        """
        Export the given object using the appropriate exporter function.
        Args:
            obj: The object to be exported.
        Returns:
            The exported object.
        Raises:
            ValueError: If the object type is not supported.
        """

        exporters = {
            BaseAuthor: cls.export_author,
            BaseDefinition: cls.export_definition,
            BaseEvent: cls.export_event,
            BaseSetting: cls.export_setting,
            BaseSyllable: cls.export_syllable,
            BaseType: cls.export_type,
            BaseWord: cls.export_word,
            BaseWordSpell: cls.export_word_spell,
        }

        exporter_func = exporters.get(obj.__class__)
        if exporter_func:
            return exporter_func(obj)

        raise ValueError(f"Unsupported object type: {obj.__class__}")

    @staticmethod
    def export_author(obj: BaseAuthor) -> str:
        """
        Prepare Author data for exporting to text file

        Returns:
            Formatted basic string.

        """
        return f"{obj.abbreviation}@{obj.full_name}@{obj.notes}"

    @staticmethod
    def export_event(obj: BaseEvent) -> str:
        """
        Prepare Event data for exporting to text file

        Returns:
            Formatted basic string.
        """
        return (
            f"{obj.id}@{obj.name}"
            f"@{obj.date.strftime('%m/%d/%Y')}@{obj.definition}"
            f"@{obj.annotation}@{obj.suffix}"
        )

    @staticmethod
    def export_syllable(obj: BaseSyllable) -> str:
        """
        Prepare Syllable data for exporting to text file

        Returns:
            Formatted basic string.
        """
        return f"{obj.name}@{obj.type}@{obj.allowed}"

    @staticmethod
    def export_setting(obj: BaseSetting) -> str:
        """
        Prepare Setting data for exporting to text file

        Returns:
            Formatted basic string.
        """
        return (
            f"{obj.date.strftime('%d.%m.%Y %H:%M:%S')}"
            f"@{obj.db_version}"
            f"@{obj.last_word_id}"
            f"@{obj.db_release}"
        )

    @staticmethod
    def export_type(obj: BaseType) -> str:
        """
        Prepare Type data for exporting to text file

        Returns:
            Formatted basic string.
        """
        return f"{obj.type}@{obj.type_x}@{obj.group}@{obj.parentable}@{obj.description or ''}"

    @staticmethod
    def export_word(obj: BaseWord) -> str:
        """
        Prepare Word data for exporting to text file

        Returns:
            Formatted basic string.
        """
        ewc = ExportWordConverter(obj)
        match = ewc.stringer(obj.match)
        tid_old = ewc.stringer(obj.tid_old)
        origin_x = ewc.stringer(obj.origin_x)
        origin = ewc.stringer(obj.origin)

        return (
            f"{obj.id_old}@{obj.type.type}@{obj.type.type_x}@{ewc.e_affixes}"
            f"@{match}@{ewc.e_source}@{ewc.e_year}@{ewc.e_rank}"
            f"@{origin}@{origin_x}@{ewc.e_usedin}@{tid_old}"
        )

    @staticmethod
    def export_definition(obj: BaseDefinition) -> str:
        """
        Prepare Definition data for exporting to text file

        Returns:
            Formatted basic string.
        """
        e_grammar = f"{obj.slots or ''}{obj.grammar_code or ''}"

        return (
            f"{obj.source_word.id_old}@{obj.position}@{obj.usage or ''}"
            f"@{e_grammar}@{obj.body}@@{obj.case_tags or ''}"
        )

    @staticmethod
    def export_word_spell(obj: BaseWord) -> str:
        """
        Prepare WordSpell data for exporting to text file

        Returns:
            Formatted basic string.
        """
        code_name = "".join(
            "0" if symbol.isupper() else "5" for symbol in str(obj.name)
        )

        return (
            f"{obj.id_old}@{obj.name}@{obj.name.lower()}@{code_name}"
            f"@{obj.event_start_id}@{obj.event_end_id if obj.event_end else 9999}@"
        )


class ExportWordConverter:
    """
    A class that provides conversion methods for exporting Word data.

    Args:
        word (BaseWord): The word to be converted.

    Properties:
        - e_source (str): Returns the source of the word.
        - e_year (str): Returns the year of the word, along with any additional notes.
        - e_usedin (str): Returns the names of the complexes in which the word is used.
        - e_affixes (str): Returns the affixes (djifoa) created from the word.
        - e_djifoa (str): Alias for the property `e_affixes`.
        - e_rank (str): Returns the rank of the word and any additional notes.

    Methods:
        - stringer(value) -> str: Convert a variable to a string.

    """

    def __init__(self, word: BaseWord):
        self.word = word

    @property
    def e_source(self) -> str:
        """
        Returns:
        """
        source = "/".join(sorted([author.abbreviation for author in self.word.authors]))
        notes: dict[str, str] = self.word.notes or {}

        return f"{source} {notes.get('author', str())}".strip()

    @property
    def e_year(self) -> str:
        """
        Returns the year of the word, along with any additional notes related to the year.

        Returns:
            str: The year of the word, along with any additional notes.
            If no year is available, an empty string is returned.
        """
        notes: dict[str, str] = self.word.notes or {}
        if self.word.year:
            return f"{self.word.year.year}{notes.get('year', str())}".strip()
        return ""

    @property
    def e_usedin(self) -> str:
        """
        Returns a string that represents the names of the complexes in which the word is used.

        Returns:
            str: A string with the names of the complexes separated by a vertical bar.
        """
        return " | ".join(cpx.name for cpx in self.word.complexes)

    @property
    def e_affixes(self) -> str:
        """
        Returns a string representation of the affixes (djifoa) created from the word.

        Returns:
            str: A string containing all affixes of the word with hyphens removed.
        """
        return " ".join(afx.name.replace("-", "") for afx in self.word.affixes).strip()

    @property
    def e_djifoa(self) -> str:
        """
        Alias for the property `e_affixes`.

        Returns:
            str: The value of the property `e_affixes`.
        """
        return self.e_affixes

    @property
    def e_rank(self) -> str:
        """
        Return the rank of the word and any additional notes about the rank.

        Returns:
            str: The rank of the word and any additional notes about the rank.
        """
        notes: dict[str, str] = self.word.notes or {}
        return f"{self.word.rank} {notes.get('rank', str())}".strip()

    @staticmethod
    def stringer(value) -> str:
        """
        Convert variable to string
        Args:
            value (any):

        Returns:
            str:
        """
        return str(value) if value else str()
