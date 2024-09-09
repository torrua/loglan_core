"""
This module contains an "Export extensions" for LOD dictionary SQL model.
Add export() function to db object for returning its text string presentation.
"""

from typing import Iterable, Callable, Type

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
        export_author: Converts a BaseAuthor object to a tuple of items.
        export_definition: Converts a BaseDefinition object to a tuple of items.
        export_event: Converts a BaseEvent object to a tuple of items.
        export_setting: Converts a BaseSetting object to a tuple of items.
        export_syllable: Converts a BaseSyllable object to a tuple of items.
        export_type: Converts a BaseType object to a tuple of items.
        export_word: Converts a BaseWord object to a tuple of items.
        export_word_spell: Converts a BaseWordSpell object to a tuple of items.

    Raises:
        ValueError: If the object type is not supported for export.
    """

    FORMAT_DATE_EVENT = "%m/%d/%Y"
    FORMAT_DATE_SETTING = "%d.%m.%Y %H:%M:%S"

    @classmethod
    def export(cls, obj, separator: str = DEFAULT_SEPARATOR) -> str:
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

        exporters: dict[Type, Callable] = {
            BaseAuthor: cls.export_author,
            BaseEvent: cls.export_event,
            BaseType: cls.export_type,
            BaseWordSpell: cls.export_word_spell,
            BaseWord: cls.export_word,
            BaseDefinition: cls.export_definition,
            BaseSetting: cls.export_setting,
            BaseSyllable: cls.export_syllable,
        }

        exporter_func = None
        for base_class, func in exporters.items():
            if isinstance(obj, base_class):
                exporter_func = func
                break

        if not exporter_func:
            raise ValueError(f"Unsupported object type: {obj.__class__}")

        items = exporter_func(obj)
        return cls.merge_by(items, separator)

    @staticmethod
    def merge_by(items: Iterable, separator: str = DEFAULT_SEPARATOR) -> str:
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
        return separator.join([str(i or "") for i in items])

    @staticmethod
    def export_author(obj: BaseAuthor) -> tuple:
        """
        Prepare Author data for exporting to text file

        Returns:
            tuple: elements for export
        """
        return obj.abbreviation, obj.full_name, obj.notes

    @classmethod
    def export_event(cls, obj: BaseEvent) -> tuple:
        """
        Prepare Event data for exporting to text file

        Returns:
            tuple: elements for export
        """
        return (
            obj.event_id,
            obj.name,
            obj.date.strftime(cls.FORMAT_DATE_EVENT),
            obj.definition,
            obj.annotation,
            obj.suffix,
        )

    @staticmethod
    def export_syllable(obj: BaseSyllable) -> tuple:
        """
        Prepare Syllable data for exporting to text file

        Returns:
            tuple: elements for export
        """
        return obj.name, obj.type_, str(obj.allowed)

    @classmethod
    def export_setting(cls, obj: BaseSetting) -> tuple:
        """
        Prepare Setting data for exporting to text file

        Returns:
            tuple: elements for export
        """
        return (
            obj.date.strftime(cls.FORMAT_DATE_SETTING),
            obj.db_version,
            obj.last_word_id,
            obj.db_release,
        )

    @staticmethod
    def export_type(obj: BaseType) -> tuple:
        """
        Prepare Type data for exporting to text file

        Returns:
            tuple: elements for export
        """
        return (
            obj.type_,
            obj.type_x,
            obj.group,
            str(obj.parentable),
            obj.description,
        )

    @staticmethod
    def export_word(obj: BaseWord) -> tuple:
        """
        Prepare Word data for exporting to text file

        Returns:
            tuple: elements for export
        """
        ewc = ExportWordConverter(obj)
        match = ewc.stringer(obj.match)
        tid_old = ewc.stringer(obj.tid_old)
        origin_x = ewc.stringer(obj.origin_x)
        origin = ewc.stringer(obj.origin)
        return (
            obj.id_old,
            obj.type.type_,
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
        )

    @staticmethod
    def export_definition(obj: BaseDefinition) -> tuple:
        """
        Prepare Definition data for exporting to text file

        Returns:
            tuple: elements for export
        """
        e_grammar = f"{obj.slots or ''}{obj.grammar_code or ''}"
        return (
            obj.source_word.id_old,
            obj.position,
            obj.usage,
            e_grammar,
            obj.body,
            "",
            obj.case_tags,
        )

    @staticmethod
    def export_word_spell(obj: BaseWordSpell) -> tuple:
        """
        Prepare WordSpell data for exporting to text file

        Returns:
            tuple: elements for export
        """
        code_name = "".join(
            "0" if symbol.isupper() else "5" for symbol in str(obj.name)
        )
        return (
            obj.id_old,
            obj.name,
            obj.name.lower(),
            code_name,
            obj.event_start_id,
            obj.event_end_id if obj.event_end else 9999,
            "",
        )
