# -*- coding: utf-8 -*-

"""
This module contains an addon for basic Word Model,
which makes it possible to specify the authors and derivatives of words
"""

from loglan_core.author import BaseAuthor
from loglan_core.connect_tables import t_connect_words
from loglan_core.word import BaseWord


class WordLinker:
    """AddonWordLinker Model"""

    @staticmethod
    def _is_parented(parent: BaseWord, child: BaseWord) -> bool:
        """
        Check, if this word is already added as a parent for this 'child'

        Args:
            parent: BaseWord
            child: BaseWord: BaseWord object to check

        Returns: bool:

        """
        return (
            parent.derivatives_query.filter(
                t_connect_words.c.child_id == child.id
            ).count()
            > 0
        )

    @classmethod
    def add_child(cls, parent: BaseWord, child: BaseWord) -> str:
        """Add derivative for the source word
        Get word from Used In and add relationship in database

        Args:
            parent: BaseWord
            child: BaseWord: Object to add

        Returns:
            String with the name of the added child (BaseWord.name)

        """
        # TODO add check if type of child is allowed to add to this word
        if not cls._is_parented(parent, child):
            parent.derivatives_query.append(child)
        return child.name

    # mark_as_parent_for
    @staticmethod
    def add_children(parent: BaseWord, children: list[BaseWord]):
        """Add derivatives for the source word
        Get words from Used In and add relationships in database

        Args:
            parent: BaseWord
            children: List[BaseWord]:

        Returns:
            None

        """
        # TODO add check if type of child is allowed to add to this word
        new_children = list(set(children) - set(parent.derivatives_query))
        if new_children:
            parent.derivatives_query.extend(new_children)

    @staticmethod
    def add_author(word: BaseWord, author: BaseAuthor) -> str:
        """Connect Author object with BaseWord object

        Args:
            word: BaseWord:
            author: BaseAuthor:

        Returns:

        """
        if (
            not word.authors_query.filter(
                BaseAuthor.abbreviation == author.abbreviation
            ).count()
            > 0
        ):
            word.authors_query.append(author)
        return author.abbreviation

    @staticmethod
    def add_authors(word: BaseWord, authors: list[BaseAuthor]):
        """Connect Author objects with BaseWord object

        Args:
            word: BaseWord
            authors: List[BaseAuthor]:

        Returns:

        """
        new_authors = list(set(authors) - set(word.authors))
        if new_authors:
            word.authors_query.extend(new_authors)
