"""
## This module contains a basic WordSource Model
"""
import re

from loglan_core.table_names import T_NAME_WORD_SOURCES


class BaseWordSource:
    """Word Source from BaseWord.origin for Prims"""

    __tablename__ = T_NAME_WORD_SOURCES
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
    ) -> tuple[int, int, str] | tuple[None, None, None]:
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
        return None, None, None  # TODO Raise Exception

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
