import pytest
from loglan_core import WordSource
from tests.data import word_sources


@pytest.mark.usefixtures("db_session")
class TestWordSource:

    def test_init_success(self):
        ws: WordSource = WordSource(word_sources[0])  # "2/3E act"
        assert ws.coincidence == 2
        assert ws.length == 3
        assert ws.language == "E"
        assert ws.transcription == "act"

    def test_str(self):
        ws: WordSource = WordSource(word_sources[0])  # "2/3E act"
        assert str(ws) == '<BaseWordSource 2/3E act>'

    def test_init_error(self):
        ws: WordSource = WordSource(word_sources[3])  # "4/4S"
        assert ws.coincidence is None
        assert ws.length is None
        assert ws.language is None
        assert ws.transcription is None

    def test_as_string(self):
        ws_0: WordSource = WordSource(word_sources[0])  # "2/3E act"
        assert ws_0.as_string == "2/3E act"

        ws_2: WordSource = WordSource(word_sources[2])  # "2/4C"
        assert ws_2.as_string == ""
