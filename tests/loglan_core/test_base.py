import pytest
from loglan_core import Word
import datetime


@pytest.mark.usefixtures("db_session")
class TestBase:

    def test_get_by_id(self, db_session):
        third_word: Word = Word.get_by_id(db_session, 3)
        assert third_word.id == 3

    def test_get_all(self, db_session):
        words = Word.get_all(db_session)
        assert len(words) == 13

    def test_export(self, db_session):
            kakto: Word = db_session.query(Word).filter(Word.name == 'kakto').first()
            assert kakto.export() == {
                'event_end_id': None, 'event_start_id': 1,
                'id': 2, 'id_old': 3880, 'match': '56%',
                'name': 'kakto', 'notes': None,
                'origin': '3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam',
                'origin_x': '', 'rank': '1.0', 'tid_old': None, 'type_id': 2,
                'year': datetime.date(1975, 1, 1)}

    def test_attributes_all(self):
        assert Word.attributes_all() == {
            'authors', 'definitions', 'relationship_derivatives',
            'event_end', 'event_start', 'parents',
            'type', 'created', 'event_end_id', 'event_start_id',
            'id', 'id_old', 'match', 'name', 'notes', 'origin',
            'origin_x', 'rank', 'tid_old', 'type_id', 'updated', 'year'}

    def test_attributes_basic(self):
        assert Word.attributes_basic() == {
            'created', 'event_end_id', 'event_start_id',
            'id', 'id_old', 'match', 'name', 'notes',
            'origin', 'origin_x', 'rank', 'tid_old',
            'type_id', 'updated', 'year'}

    def test_attributes_extended(self):
        assert Word.attributes_extended() == {
            'authors', 'definitions', 'relationship_derivatives',
            'event_end', 'event_start',
            'parents', 'type', 'created', 'id', 'id_old',
            'match', 'name', 'notes', 'origin',
            'origin_x', 'rank', 'updated', 'year'}

    def test_relationships(self):
        assert Word.relationships() == {
            'authors', 'definitions', 'relationship_derivatives',
            'event_end', 'event_start', 'parents', 'type'}

    def test_foreign_keys(self):
        assert Word.foreign_keys() == {
            'event_start_id', 'tid_old', 'event_end_id', 'type_id'}

    def test_non_foreign_keys(self):
        assert Word.non_foreign_keys() == {
            'TID_old', 'created', 'id', 'id_old', 'match', 'name',
            'notes', 'origin', 'origin_x', 'rank', 'updated', 'year'}
