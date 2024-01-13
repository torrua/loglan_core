"""
This module contains an addon for basic Word Model,
which makes it possible to work with word's sources
"""

from sqlalchemy import select
from sqlalchemy.sql.selectable import Select

from loglan_core.type import BaseType
from loglan_core.word import BaseWord
from loglan_core.word_source import BaseWordSource


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
    def get_sources_prim(cls, word: BaseWord):
        """

        Returns:

        """
        # existing_prim_types = ["C", "D", "I", "L", "N", "O", "S", ]

        if not word.type.group == "Prim":
            return None

        if word.type.type == "C-Prim":
            return cls._get_sources_c_prim(word)

        # TODO сделать вывод унифицированным
        return f"{word.name}: {word.origin}{' < ' + word.origin_x if word.origin_x else ''}"

    @staticmethod
    def _get_sources_c_prim(word: BaseWord) -> list[BaseWordSource] | None:
        """
        Returns:
        """
        if word.type.type != "C-Prim":
            return None

        sources = str(word.origin).split(" | ")

        return [BaseWordSource(source) for source in sources]

    @classmethod
    def get_sources_cpx(
        cls, word: BaseWord, as_str: bool = False
    ) -> Select[tuple[BaseWord]] | list[str]:
        """Extract source words from self.origin field accordingly
        Args:
            word (BaseWord):
            as_str (bool): return BaseWord objects if False else as simple str
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
    def words_from_source_cpx(cls, sources: list[str]) -> Select[tuple[BaseWord]]:
        """

        Args:
            sources:

        Returns:

        """
        exclude_type_ids = BaseType.by_property(
            ["LW", "Cpd"], id_only=True
        ).scalar_subquery()
        return (
            select(BaseWord)
            .filter(BaseWord.name.in_(sources))
            .filter(BaseWord.type_id.notin_(exclude_type_ids))
        )

    @staticmethod
    def _prepare_sources_cpx(word: BaseWord) -> list[str]:
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
        cls, word: BaseWord, as_str: bool = False
    ) -> Select[tuple[BaseWord]] | list[str]:
        """Extract source words from self.origin field accordingly

        Args:
          word: BaseWord:
          as_str: bool: return BaseWord objects if False else as simple str
          (Default value = False)

        Returns:
          List of words from which the self.name was created
        """

        if not word.type.type == "Cpd":
            return []

        sources = cls._prepare_sources_cpd(word)
        return sources if as_str else cls.words_from_source_cpd(sources)

    @staticmethod
    def _prepare_sources_cpd(word: BaseWord) -> list[str]:
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

    @staticmethod
    def words_from_source_cpd(sources: list[str]) -> Select[tuple[BaseWord]]:
        """

        Args:
            sources:

        Returns:

        """

        type_ids = BaseType.by_property(["LW", "Cpd"], id_only=True).scalar_subquery()
        return (
            select(BaseWord)
            .filter(BaseWord.name.in_(sources))
            .filter(BaseWord.type_id.in_(type_ids))
        )
