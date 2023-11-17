# -*- coding: utf-8 -*-
# pylint: disable=R0201, R0903

"""Export Model unit tests."""

import pytest

from loglan_core.addons.exporter import Exporter
from loglan_core import Author, Word, Event, Syllable, Setting, Type, Definition

@pytest.mark.usefixtures("db_session")
class TestExporter:

    e = Exporter()

    def test_wrong_type_export(self):
        class TestClass:
            pass

        with pytest.raises(ValueError) as _:
            self.e.export(TestClass())

    def test_export_word(self, db_session):
        """Test Word.export() method"""
        obj = db_session.query(Word).filter(Word.name == "kakto").scalar()
        result = self.e.export(obj)
        assert result == (
            '3880@C-Prim@Predicate@kak kao@56%@L4@1975@1.0'
            '@3/3R akt | 4/4S acto | 3/3F '
            'acte | 2/3E act | 2/3H kam@@prukao@'
        )

        obj.year = None
        result = self.e.export(obj)
        assert result == (
            '3880@C-Prim@Predicate@kak kao@56%@L4@@1.0'
            '@3/3R akt | 4/4S acto | 3/3F '
            'acte | 2/3E act | 2/3H kam@@prukao@'
        )

    def test_export_author(self, db_session):
        """Test Author.export() method"""
        obj = db_session.query(Author).filter(Author.abbreviation == "JCB").scalar()
        result = self.e.export(obj)
        assert result == 'JCB@James Cooke Brown@'

    def test_export_event(self, db_session):
        """Test Event.export() method"""
        obj = db_session.query(Event).filter(Event.annotation == "Initial").scalar()
        result = self.e.export(obj)
        assert result == '1@Start@01/01/1975@The initial vocabulary before updates.@Initial@INIT'

    def test_export_syllable(self, db_session):
        """Test Syllable.export() method"""
        obj = db_session.query(Syllable).filter(Syllable.name == "vr").scalar()
        result = self.e.export(obj)
        assert result == "vr@InitialCC@True"

    def test_export_setting(self, db_session):
        """Test Setting.export() method"""
        obj = db_session.query(Setting).filter(Setting.db_release == "4.5.9").scalar()
        result = self.e.export(obj)
        assert result == "09.10.2020 09:10:20@2@10141@4.5.9"

    def test_export_type(self, db_session):
        """Test Type.export() method"""
        obj = db_session.query(Type).filter(Type.type == "2-Cpx").scalar()
        result = self.e.export(obj)
        assert result == "2-Cpx@Predicate@Cpx@True@Two-term Complex " \
                         "E.g. flicea, from fli(du)+ce(nj)a=liquid-become."


    def test_export_definition(self, db_session):
        """Test Definition.export() method"""
        obj = db_session.query(Definition).filter(Definition.body == 'K «test»/«examine» B for P with test V.').scalar()
        result = self.e.export(obj)
        assert result == "7191@1@@4v@K «test»/«examine» B for P with test V.@@K-BPV"


    def test_export_word_spell(self, db_session):
        """Test WordSpell.export() method"""
        obj = db_session.query(Word).filter(Word.name == "prukao").scalar()
        result = self.e.export_word_spell(obj)
        assert result == "7191@prukao@prukao@555555@3@9999@"
