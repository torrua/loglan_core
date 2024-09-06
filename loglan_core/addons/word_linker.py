"""
This module offers the ability to establish relationships
between BaseWord instances and BaseAuthor instances.
This is done via the WordLinker class which provides methods to check and add
parent-child relationships between words and associate authors with words.
"""

from loglan_core.author import BaseAuthor
from loglan_core.word import BaseWord


class WordLinker:
    """
    This class provides methods to manage parent-child
    relationships between words and to associate authors with words.
    """

    @classmethod
    def add_child(cls, parent: BaseWord, child: BaseWord) -> str:
        """
        Associates a 'child' word with a 'parent' word,
        indicating that the child is derived from the parent.

        Args:
            parent (BaseWord): The original word.
            child (BaseWord): The word derived from the parent.

        Returns:
            str: The name of the child word.

        Raises:
            TypeError: If the child word is not parentable.
        """

        if not child.type.parentable:
            raise TypeError(f"{child} is not parentable")

        if child not in parent.derivatives:
            parent.derivatives.append(child)
        return child.name

    # mark_as_parent_for
    @staticmethod
    def add_children(parent: BaseWord, children: list[BaseWord]):
        """
        Associates multiple 'children' words with a 'parent' word,
        indicating that those children are derived from the parent.

        Args:
            parent (BaseWord): The original word.
            children (list[BaseWord]): The words derived from the parent.

        Raises:
            TypeError: If any of the children words are not parentable.
        """
        new_children = list(set(children) - set(parent.derivatives))

        if not all(child.type.parentable for child in new_children):
            raise TypeError(f"At least some of {new_children} are not parentable")

        if new_children:
            parent.derivatives.extend(new_children)

    @staticmethod
    def add_author(word: BaseWord, author: BaseAuthor) -> str:
        """
        Associates an 'author' with a 'word', indicating
        that the author has contributed to the word.

        Args:
            word (BaseWord): The word to be associated with the author.
            author (BaseAuthor): The author to be associated with the word.

        Returns:
            str: The abbreviation of the author's name.
        """
        if author not in word.authors:
            word.authors.append(author)
        return author.abbreviation

    @staticmethod
    def add_authors(word: BaseWord, authors: list[BaseAuthor]):
        """
        Associates multiple 'authors' with a 'word',
        indicating that these authors have contributed to the word.

        Args:
            word (BaseWord): The word to be associated with the authors.
            authors (list[BaseAuthor]): The authors to be associated with the word.
        """
        new_authors = list(set(authors) - set(word.authors))
        if new_authors:
            word.authors.extend(new_authors)
