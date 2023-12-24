# -*- coding: utf-8 -*-
"""
This module contains an "Export extensions" for LOD dictionary SQL model.
Add export() function to db object for returning its text string presentation.
"""
from typing import Iterable

from loglan_core.addons.export_word_converter import ExportWordConverter
from loglan_core.author import BaseAuthor
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.setting import BaseSetting
from loglan_core.syllable import BaseSyllable
from loglan_core.type import BaseType
from loglan_core.word import BaseWord
from loglan_core.word_spell import BaseWordSpell

DEFAULT_SEPARATOR = "@"


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
    def export(
        cls,
        obj,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Export the given object using the appropriate exporter function.
        Args:
            obj: The object to be exported.
            separator: The separator to be used in the exported string.
        Returns:
            The exported object.
        Raises:
            ValueError: If the object type is not supported.
        """

        exporters = {
            BaseAuthor: cls.export_author,
            BaseEvent: cls.export_event,
            BaseType: cls.export_type,
            BaseWord: cls.export_word,
            BaseWordSpell: cls.export_word_spell,
            BaseDefinition: cls.export_definition,
            BaseSetting: cls.export_setting,
            BaseSyllable: cls.export_syllable,
        }

        if obj.__class__ not in exporters:
            raise ValueError(f"Unsupported object type: {obj.__class__}")

        exporter_func = exporters.get(obj.__class__)
        return exporter_func(obj, separator)

    @staticmethod
    def value_or_empty_string(value):
        """
        Returns the given value if it's truthy, otherwise returns an empty string.
        Parameters:
            value (any): The value to check for truthiness.
        Returns:
            any | str: The original value if truthy, or an empty string if not.
        """
        return value if value else ""

    ves = value_or_empty_string

    @staticmethod
    def merge_by(
        items: Iterable,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Merges a list of items into a single string, separated by the
        specified separator.
        Parameters:
            items (list): The list of items to merge.
            separator (str): The string to use as a separator, with a default
                         value.
        Returns:
        str: The resulting string after joining the items.
        """
        return separator.join([str(i) for i in items])

    @classmethod
    def export_author(
        cls,
        obj: BaseAuthor,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Author data for exporting to text file

        Returns:
            Formatted basic string.

        """
        items = [obj.abbreviation, obj.full_name, obj.notes]
        return cls.merge_by(items, separator)

    @classmethod
    def export_event(
        cls,
        obj: BaseEvent,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Event data for exporting to text file

        Returns:
            Formatted basic string.
        """
        items = [
            obj.id,
            obj.name,
            obj.date.strftime("%m/%d/%Y"),
            obj.definition,
            obj.annotation,
            obj.suffix,
        ]
        return cls.merge_by(items, separator)

    @classmethod
    def export_syllable(
        cls,
        obj: BaseSyllable,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Syllable data for exporting to text file

        Returns:
            Formatted basic string.
        """
        items = [obj.name, obj.type, obj.allowed]
        return cls.merge_by(items, separator)

    @classmethod
    def export_setting(
        cls,
        obj: BaseSetting,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Setting data for exporting to text file

        Returns:
            Formatted basic string.
        """
        items = [
            obj.date.strftime("%d.%m.%Y %H:%M:%S"),
            obj.db_version,
            obj.last_word_id,
            obj.db_release,
        ]
        return cls.merge_by(items, separator)

    @classmethod
    def export_type(
        cls,
        obj: BaseType,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Type data for exporting to text file

        Returns:
            Formatted basic string.
        """
        items = [
            obj.type,
            obj.type_x,
            obj.group,
            obj.parentable,
            cls.ves(obj.description),
        ]
        return cls.merge_by(items, separator)

    @classmethod
    def export_word(
        cls,
        obj: BaseWord,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
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
        items = [
            obj.id_old,
            obj.type.type,
            obj.type.type_x,
            ewc.e_affixes,
            match,
            ewc.e_source,
            ewc.e_year,
            ewc.e_rank,
            origin,
            origin_x,
            ewc.e_usedin,
            tid_old,
        ]
        return cls.merge_by(items, separator)

    @classmethod
    def export_definition(
        cls,
        obj: BaseDefinition,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare Definition data for exporting to text file

        Returns:
            Formatted basic string.
        """
        e_grammar = f"{obj.slots or ''}{obj.grammar_code or ''}"
        items = [
            obj.source_word.id_old,
            obj.position,
            cls.ves(obj.usage),
            e_grammar,
            obj.body,
            "",
            cls.ves(obj.case_tags),
        ]
        return cls.merge_by(items, separator)

    @classmethod
    def export_word_spell(
        cls,
        obj: BaseWordSpell,
        separator: str = DEFAULT_SEPARATOR,
    ) -> str:
        """
        Prepare WordSpell data for exporting to text file

        Returns:
            Formatted basic string.
        """
        code_name = "".join(
            "0" if symbol.isupper() else "5" for symbol in str(obj.name)
        )
        items = [
            obj.id_old,
            obj.name,
            obj.name.lower(),
            code_name,
            obj.event_start_id,
            obj.event_end_id if obj.event_end else 9999,
            "",
        ]
        return cls.merge_by(items, separator)
