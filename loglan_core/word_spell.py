# pylint: disable=too-many-ancestors
"""
This module contains the BaseWordSpell model.

The BaseWordSpell class exists primarily for backward compatibility with legacy LOD
(Loglan Online Dictionary) databases and exports. In historical LOD datasets, word
spellings and case variants were represented through specialized spell models and
export formats (see Exporter.export_word_spell).

Modern consumers should generally use BaseWord (or Word) directly, but BaseWordSpell
is preserved to ensure compatibility with legacy schemas, fixtures, and external tools.
"""

from .word import BaseWord


class BaseWordSpell(BaseWord):
    """BaseWordSpell model.

    Inherits from :class:`BaseWord`. Retained for backwards compatibility with legacy
    Loglan dictionary export workflows and historical schema designs where word
    spellings were distinguished with specific format codes.
    """
