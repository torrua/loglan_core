'''
# -*- coding: utf-8 -*-
"""
This module contains an addon for basic Word Model,
which makes it possible to specify the authors and derivatives of words
"""

from typing import List


from loglan_core.author import BaseAuthor
from loglan_core.connect_tables import t_connect_words
from loglan_core.word import BaseWord


class AddonWordLinker:
    """AddonWordLinker Model"""
    _contribution = None

    def _is_parented(self, child: BaseWord) -> bool:
        """
        Check, if this word is already added as a parent for this 'child'

        Args:
            child: BaseWord: BaseWord object to check

        Returns: bool:

        """
        return bool(self._derivatives.filter(t_connect_words.c.child_id == child.id).count() > 0)

    # mark_as_parent_for
    def add_child(self, child: BaseWord) -> str:
        """Add derivative for the source word
        Get word from Used In and add relationship in database

        Args:
          child: BaseWord: Object to add

        Returns:
            String with the name of the added child (BaseWord.name)

        """
        # TODO add check if type of child is allowed to add to this word
        if not self._is_parented(child):
            self._derivatives.append(child)
        return child.name

    # mark_as_parent_for
    def add_children(self, children: List[BaseWord]):
        """Add derivatives for the source word
        Get words from Used In and add relationships in database

        Args:
          children: List[BaseWord]:

        Returns:
          None

        """
        # TODO add check if type of child is allowed to add to this word
        new_children = list(set(children) - set(self._derivatives))
        _ = self._derivatives.extend(new_children) if new_children else None

    def add_author(self, author: BaseAuthor) -> str:
        """Connect Author object with BaseWord object

        Args:
          author: BaseAuthor:

        Returns:

        """
        if not self.authors_query.filter(BaseAuthor.abbreviation == author.abbreviation).count() > 0:
            self.authors_query.append(author)
        return author.abbreviation

    def add_authors(self, authors: List[BaseAuthor]):
        """Connect Author objects with BaseWord object

        Args:
          authors: List[BaseAuthor]:

        Returns:

        """
        new_authors = list(set(authors) - set(self.authors))
        _ = self._authors.extend(new_authors) if new_authors else None
'''