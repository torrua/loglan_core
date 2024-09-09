"""
This module contains an addon for basic Word Model,
which makes it possible to work with word's sources
"""

from __future__ import annotations

import re
from typing import Iterable

from sqlalchemy import select, or_
from sqlalchemy.sql.selectable import Select

from loglan_core import Type
from loglan_core import Word


class WordSource:
    """Word Source from Word.origin for Prims"""

    PATTERN_SOURCE = r"\d+\/\d+\w"

    LANGUAGES = {
        "E": "English",
        "C": "Chinese",
        "H": "Hindi",
        "R": "Russian",
        "S": "Spanish",
        "F": "French",
        "J": "Japanese",
        "G": "German",
    }

    def __init__(self, source):
        compatibility_search = re.search(self.PATTERN_SOURCE, source)
        self.coincidence, self.length, self.language = self.parse_source(
            compatibility_search
        )

        transcription_search = re.search(rf"(?!{self.PATTERN_SOURCE}) .+", source)
        self.transcription = (
            str(transcription_search[0]).strip() if transcription_search else None
        )

    def __str__(self):
        """
        Returns:
        """
        return f"<{self.__class__.__name__} {self.as_string}>"

    @staticmethod
    def parse_source(
        compatibility_search,
    ) -> tuple[int, int, str]:
        """

        Args:
            compatibility_search:

        Returns:

        """
        if compatibility_search:
            coincidence: int = int(compatibility_search[0][:-1].split("/")[0])
            length: int = int(compatibility_search[0][:-1].split("/")[1])
            language: str = compatibility_search[0][-1:]
            return coincidence, length, language
        raise ValueError("No compatible source found")

    @property
    def as_string(self) -> str:
        """
        Format WordSource as string, for example, '3/5R mesto'
        Returns:
            str
        """
        if not all([self.coincidence, self.length, self.language, self.transcription]):
            return str()
        return f"{self.coincidence}/{self.length}{self.language} {self.transcription}"


class WordSourcer:
    """WordSourcer Model"""

    # these primes have switched djifoas like 'flo' for 'folma'
    switch_prims = [
        "canli",
        "farfu",
        "folma",
        "forli",
        "kutla",
        "marka",
        "mordu",
        "sanca",
        "sordi",
        "suksi",
        "surna",
    ]

    @classmethod
    def get_sources_prim(cls, word: Word):
        """

        Returns:

        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not word.type.group == "Prim":
            return None

        if word.type.type_ == "C-Prim":
            return cls._get_sources_c_prim(word)

        return f"{word.name}: {word.origin}{' < ' + word.origin_x if word.origin_x else ''}"

    @staticmethod
    def _get_sources_c_prim(word: Word) -> list[WordSource] | None:
        """
        Returns:
        """
        if word.type.type_ != "C-Prim":
            return None

        sources = str(word.origin).split(" | ")

        return [WordSource(source) for source in sources]

    @classmethod
    def get_sources_cpx(
        cls, word: Word, as_str: bool = False
    ) -> Select[tuple[Word]] | list[str]:
        """Extract source words from self.origin field accordingly
        Args:
            word (Word):
            as_str (bool): return Word objects if False else as simple str
            (Default value = False)
        Example:
            'foldjacea' > ['forli', 'djano', 'cenja']
        Returns:
            List of words from which the self.name was created

        """

        if not word.type.group == "Cpx":
            return []

        sources = cls._prepare_sources_cpx(word)
        return sources if as_str else cls.words_from_source_cpx(sources)

    @classmethod
    def words_from_source_cpx(cls, sources: list[str]) -> Select[tuple[Word]]:
        """

        Args:
            sources:

        Returns:

        """
        exclude_ids = cls.get_type_ids(types=("LW", "Cpd"))

        return (
            select(Word)
            .filter(Word.name.in_(sources))
            .filter(Word.type_id.notin_(exclude_ids))
        )

    @classmethod
    def get_type_ids(cls, types: Iterable[str]):
        """
        Get ids of specific types from provided list

        Args:
            types (Iterable[str]): List of types to get

        Returns:
            Subquery
        """
        return (
            select(Type.id)
            .filter(
                or_(
                    Type.type_.in_(types),
                    Type.type_x.in_(types),
                    Type.group.in_(types),
                )
            )
            .scalar_subquery()
        )

    @staticmethod
    def _prepare_sources_cpx(word: Word) -> list[str]:
        """
        Returns:
        """
        if not word.origin:
            return []

        sources_str = word.origin.replace("(", "").replace(")", "").replace("/", "")
        sources_list = sources_str.split("+")
        sources = [
            s if not s.endswith(("r", "h")) else s[:-1]
            for s in sources_list
            if s not in ["y", "r", "n"]
        ]
        return sources

    @classmethod
    def get_sources_cpd(
        cls, word: Word, as_str: bool = False
    ) -> Select[tuple[Word]] | list[str]:
        """Extract source words from self.origin field accordingly

        Args:
          word: Word:
          as_str: bool: return Word objects if False else as simple str
          (Default value = False)

        Returns:
          List of words from which the self.name was created
        """

        if not word.type.type_ == "Cpd":
            return []

        sources = cls._prepare_sources_cpd(word)
        return sources if as_str else cls.words_from_source_cpd(sources)

    @staticmethod
    def _prepare_sources_cpd(word: Word) -> list[str]:
        """
        Returns:
        """
        if not word.origin:
            return []

        sources_str = (
            word.origin.replace("(", "")
            .replace(")", "")
            .replace("/", "")
            .replace("-", "")
        )
        sources = [s.strip() for s in sources_str.split("+") if s]
        return sources

    @classmethod
    def words_from_source_cpd(cls, sources: list[str]) -> Select[tuple[Word]]:
        """

        Args:
            sources:

        Returns:

        """

        type_ids = cls.get_type_ids(types=("LW", "Cpd"))

        return (
            select(Word)
            .filter(Word.name.in_(sources))
            .filter(Word.type_id.in_(type_ids))
        )
