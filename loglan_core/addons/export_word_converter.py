"""
This module contains ExportWordConverter for Word model of LOD.
"""

from loglan_core.word import BaseWord


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
            return f"{self.word.year.year} {notes.get('year', str())}".strip()
        return ""

    @property
    def e_usedin(self) -> str:
        """
        Returns a string that represents the names of the complexes in which the word is used.

        Returns:
            str: A string with the names of the complexes separated by a vertical bar.
        """
        return " | ".join(
            cpx.name for cpx in self.word.derivatives if cpx.type.group == "Cpx"
        )

    @property
    def e_affixes(self) -> str:
        """
        Returns a string representation of the affixes (djifoa) created from the word.

        Returns:
            str: A string containing all affixes of the word with hyphens removed.
        """
        return " ".join(
            afx.name.replace("-", "")
            for afx in self.word.derivatives
            if afx.type.type_x == "Affix"
        ).strip()

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
