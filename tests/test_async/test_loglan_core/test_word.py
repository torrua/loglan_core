import pytest
from sqlalchemy import select
from loglan_core import Word, Type, Event, WordSelector


@pytest.mark.usefixtures("session")
class TestAsyncWord:
    async def test_str(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        assert str(kakto) == "<BaseWord ID 2 kakto>"

    async def test_type_relationship(self, session):
        prukao = await WordSelector().by_name("prukao").scalar_async(session)
        assert prukao is not None
        word_type = await prukao.awaitable_attrs.type
        assert isinstance(word_type, Type)
        assert word_type.group == "Cpx"

    async def test_event_start_relationship(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        event_start = await kakto.awaitable_attrs.event_start
        assert isinstance(event_start, Event)
        assert event_start.event_id == 1

    async def test_authors_relationship(self, session):
        prukao = await WordSelector().by_name("prukao").scalar_async(session)
        assert prukao is not None
        authors = await prukao.awaitable_attrs.authors
        assert len(authors) == 2

    async def test_definitions_relationship(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        definitions = await kakto.awaitable_attrs.definitions
        assert len(definitions) == 5

    async def test_derivatives_relationship(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        derivatives = await kakto.awaitable_attrs.derivatives
        assert len(derivatives) == 3

    async def test_parents_relationship(self, session):
        prukao = await WordSelector().by_name("prukao").scalar_async(session)
        assert prukao is not None
        parents = await prukao.awaitable_attrs.parents
        parent_names = [p.name for p in parents]
        assert "kakto" in parent_names

    async def test_affixes_hybrid_property(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        await kakto.awaitable_attrs.derivatives
        assert len(kakto.affixes) == 2
        assert isinstance(kakto.affixes[0], Word)

    async def test_complexes_hybrid_property(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        await kakto.awaitable_attrs.derivatives
        assert len(kakto.complexes) == 1
        assert isinstance(kakto.complexes[0], Word)

    async def test_keys_property(self, session):
        kakto = await WordSelector().by_name("kakto").scalar_async(session)
        assert kakto is not None
        # ensure definitions and their keys are loaded
        definitions = await kakto.awaitable_attrs.definitions
        for d in definitions:
            await d.awaitable_attrs.keys
        assert len(kakto.keys) == 5
        assert [k.word for k in kakto.keys] == [
            "act",
            "activity",
            "actor",
            "end",
            "undertake",
        ]

    async def test_complexes_and_affixes_async_sql_filter(self, session):
        cpx_stmt = select(Word).where(Word.complexes.any())
        words_with_cpx = (await session.scalars(cpx_stmt)).all()
        assert "kakto" in {w.name for w in words_with_cpx}

        affix_stmt = select(Word).where(Word.affixes.any(Word.name == "kak"))
        words_with_kak = (await session.scalars(affix_stmt)).all()
        assert len(words_with_kak) == 1
        assert words_with_kak[0].name == "kakto"
