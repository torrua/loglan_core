"""
Tests for foreign key ON DELETE rules and referential integrity.
"""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from loglan_core import (
    Word,
    Author,
    Key,
    Type,
    Event,
    Definition,
    t_connect_authors,
    t_connect_words,
    t_connect_keys,
)


@pytest.mark.usefixtures("db_session")
class TestReferentialIntegrity:
    """Tests verifying foreign key constraints and ON DELETE cascades."""

    def test_ondelete_metadata(self):
        """Verify ondelete attributes in SQLAlchemy schema metadata."""
        # t_connect_authors
        for col in (t_connect_authors.c.AID, t_connect_authors.c.WID):
            fk = next(iter(col.foreign_keys))
            assert fk.ondelete == "CASCADE"

        # t_connect_words
        for col in (t_connect_words.c.parent_id, t_connect_words.c.child_id):
            fk = next(iter(col.foreign_keys))
            assert fk.ondelete == "CASCADE"

        # t_connect_keys
        for col in (t_connect_keys.c.KID, t_connect_keys.c.DID):
            fk = next(iter(col.foreign_keys))
            assert fk.ondelete == "CASCADE"

        # definition.word_id
        def_word_id_fk = next(iter(Definition.__table__.c.word_id.foreign_keys))
        assert def_word_id_fk.ondelete == "CASCADE"

        # word foreign keys
        type_fk = next(iter(Word.__table__.c.type.foreign_keys))
        assert type_fk.ondelete == "RESTRICT"

        ev_start_fk = next(iter(Word.__table__.c.event_start.foreign_keys))
        assert ev_start_fk.ondelete == "RESTRICT"

        ev_end_fk = next(iter(Word.__table__.c.event_end.foreign_keys))
        assert ev_end_fk.ondelete == "SET NULL"

    def test_delete_author_cascades_only_connection(self, db_session):
        """Deleting an author deletes only the junction row; the word remains."""
        author = db_session.get(Author, 1)
        assert author is not None
        associated_words = list(author.contribution)
        assert len(associated_words) > 0
        word_id = associated_words[0].id

        # Delete author
        db_session.delete(author)
        db_session.commit()

        # Word must still exist in DB
        word = db_session.get(Word, word_id)
        assert word is not None

        # Link in junction table must be gone
        links = db_session.execute(
            select(t_connect_authors).where(t_connect_authors.c.AID == 1)
        ).all()
        assert len(links) == 0

    def test_delete_key_cascades_only_connection(self, db_session):
        """Deleting a key deletes only the junction row; definition and word remain."""
        key = db_session.scalars(select(Key).where(Key.word == "test")).first()
        assert key is not None
        key_id = key.id

        # Verify key has definitions
        assert len(key.definitions) > 0
        definition_id = key.definitions[0].id

        # Delete key
        db_session.delete(key)
        db_session.commit()

        # Definition must still exist
        definition = db_session.get(Definition, definition_id)
        assert definition is not None

        # Link in junction table must be gone
        links = db_session.execute(
            select(t_connect_keys).where(t_connect_keys.c.KID == key_id)
        ).all()
        assert len(links) == 0

    def test_delete_type_restricted(self, db_session):
        """Deleting a Type currently used by words raises IntegrityError."""
        type_used = db_session.get(Type, 1)
        assert type_used is not None

        db_session.delete(type_used)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_delete_event_start_restricted(self, db_session):
        """Deleting an Event used as event_start raises IntegrityError."""
        event_used = db_session.scalars(
            select(Event).where(Event.event_id == 1)
        ).first()
        assert event_used is not None

        db_session.delete(event_used)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
