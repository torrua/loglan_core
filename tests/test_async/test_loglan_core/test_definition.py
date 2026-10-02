import pytest
from loglan_core import Definition, Key, Word, DefinitionSelector


@pytest.mark.usefixtures("session")
class TestAsyncDefinition:
    async def test_keys_relationship(self, session):
        definition = await DefinitionSelector().filter_by(id=1).scalar_async(session)
        assert definition is not None
        keys = await definition.awaitable_attrs.keys
        assert len(keys) == 2
        key_words = [k.word for k in keys]
        assert "test" in key_words

    async def test_source_word_relationship(self, session):
        definition = await DefinitionSelector().filter_by(id=1).scalar_async(session)
        assert definition is not None
        source_word = await definition.awaitable_attrs.source_word
        assert isinstance(source_word, Word)
        assert source_word.name == "prukao"

    async def test_grammar(self, session):
        definition = await DefinitionSelector().filter_by(id=1).scalar_async(session)
        assert definition is not None
        assert definition.grammar == "(4v)"
