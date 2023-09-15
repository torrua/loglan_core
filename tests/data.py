# -*- coding: utf-8 -*-
"""Data for test_models"""

import datetime
from loglan_core import Word, Definition, Type, Event, Author, Key

# ===== KEYS ===================================================================
key_1 = {'word': 'examine', 'language': 'en', }
key_2 = {'word': 'test', 'language': 'en', }
key_3 = {'word': 'tester', 'language': 'en', }
key_4 = {'word': 'testable', 'language': 'en', }
key_5 = {'word': 'testee', 'language': 'en', }
key_6 = {'word': 'examination', 'language': 'en', }
key_7 = {'word': 'act', 'language': 'en', }
key_8 = {'word': 'undertake', 'language': 'en', }
key_9 = {'word': 'actor', 'language': 'en', }
key_10 = {'word': 'end', 'language': 'en', }
key_11 = {'word': 'activity', 'language': 'en', }
keys = [key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10, key_11]
keys_pair = (keys, Key)

un_key_1 = {'word': 'test', 'language': 'fr', }
un_key_2 = {'word': 'test', 'language': 'es', }
un_keys = [un_key_1, un_key_2, ]

# ===== AUTHORS ================================================================
author_1 = {'notes': 'The printed-on-paper book, 1975 version of the dictionary.', 'abbreviation': 'L4', 'full_name': 'Loglan 4&5', }
author_2 = {'notes': '', 'abbreviation': 'JCB', 'full_name': 'James Cooke Brown', }
authors = [author_1, author_2]

# ===== TYPES ==================================================================
type_1 = {'description': 'Two-term Complex E.g. flicea, from fli(du)+ce(nj)a=liquid-become.', 'group': 'Cpx', 'type': '2-Cpx', 'parentable': True, 'type_x': 'Predicate', }
type_2 = {'description': 'Composite Primitives, drawn from several target languages in a way that might make them recognizable in most of them. (See Loglan 1 Section 6.3.)', 'group': 'Prim', 'type': 'C-Prim', 'parentable': False, 'type_x': 'Predicate', }
type_3 = {'description': 'Affix.', 'group': 'Little', 'type': 'Afx', 'parentable': True, 'type_x': 'Affix', }
types = [type_1, type_2, type_3]

# ===== WORDS ==================================================================
word_1 = {'notes': None, 'tid_old': None, 'id_old': 3869, 'name': 'kak', 'type_id': 3, 'origin': 'kak(to)', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
word_2 = {'notes': None, 'tid_old': None, 'id_old': 3880, 'name': 'kakto', 'type_id': 2, 'origin': '3/3R akt | 4/4S acto | 3/3F acte | 2/3E act | 2/3H kam', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '56%', 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
word_3 = {'notes': {'author': '(?)', 'year': '(?)'}, 'tid_old': None, 'id_old': 9983, 'name': 'kao', 'type_id': 3, 'origin': 'ka(kt)o', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '', 'rank': '7+?', 'year': datetime.date(1988, 1, 1)}
word_4 = {'notes': None, 'tid_old': None, 'id_old': 7188, 'name': 'pru', 'type_id': 3, 'origin': 'pru(ci)', 'event_start_id': 3, 'origin_x': '', 'event_end_id': None, 'match': '', 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
word_5 = {'notes': None, 'tid_old': None, 'id_old': 7190, 'name': 'pruci', 'type_id': 2, 'origin': '3/4E prove | 2/4C sh yen | 3/6S prueba | 2/5R proba | 2/5F epreuve | 2/5G probe | 2/6J tameshi', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '49%', 'rank': '1.9', 'year': datetime.date(1975, 1, 1)}
word_6 = {'notes': None, 'tid_old': None, 'id_old': 7191, 'name': 'prukao', 'type_id': 1, 'origin': 'pru(ci)+ka(kt)o', 'event_start_id': 3, 'origin_x': 'test act', 'event_end_id': None, 'match': '', 'rank': '1.9', 'year': datetime.date(1975, 1, 1)}
words = [word_1, word_2, word_3, word_4, word_5, word_6]

# ===== DEFINITIONS ============================================================
definition_1 = {'position': 1, 'notes': None, 'body': 'K «test»/«examine» B for P with test V.', 'slots': 4, 'usage': '', 'word_id': 6, 'language': 'en', 'case_tags': 'K-BPV', 'grammar_code': 'v'}
definition_2 = {'position': 2, 'notes': None, 'body': 'a «tester», one who uses tests.', 'slots': None, 'usage': '', 'word_id': 6, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_3 = {'position': 3, 'notes': None, 'body': '«testable», of one who/that which is -ed.', 'slots': None, 'usage': 'nu %', 'word_id': 6, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_4 = {'position': 4, 'notes': None, 'body': 'a «testee», one who is -ed.', 'slots': None, 'usage': 'nu %', 'word_id': 6, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_5 = {'position': 5, 'notes': None, 'body': 'a «test»/«examination», an act of testing.', 'slots': None, 'usage': 'po %', 'word_id': 6, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_6 = {'position': 1, 'notes': None, 'body': 'K «act»/«undertake» action V with end/purpose P.', 'slots': 3, 'usage': '', 'word_id': 2, 'language': 'en', 'case_tags': 'K-VP', 'grammar_code': 'v'}
definition_7 = {'position': 2, 'notes': None, 'body': 'an «actor», one who seeks ends, general term.', 'slots': None, 'usage': '', 'word_id': 2, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_8 = {'position': 3, 'notes': None, 'body': 'an «end», what an actor seeks, but see {furkao}.', 'slots': None, 'usage': 'fu %', 'word_id': 2, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_9 = {'position': 4, 'notes': None, 'body': 'an «act», what an actor does, but see {nurkao}.', 'slots': None, 'usage': 'nu %', 'word_id': 2, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_10 = {'position': 5, 'notes': None, 'body': 'an «activity», specific instance.', 'slots': None, 'usage': 'po %', 'word_id': 2, 'language': 'en', 'case_tags': '', 'grammar_code': 'n'}
definition_11 = {'position': 1, 'notes': None, 'body': 'V is a «test»/«examination» for property B in any member of class F.', 'slots': 3, 'usage': '', 'word_id': 5, 'language': 'en', 'case_tags': 'V-BF', 'grammar_code': 'n'}
definition_12 = {'position': 2, 'notes': None, 'body': '«test», test for ... a property ... in a member of ....', 'slots': None, 'usage': '', 'word_id': 5, 'language': 'en', 'case_tags': '', 'grammar_code': 'vt'}
definition_13 = {'position': 3, 'notes': None, 'body': '«testable», of classes with -able members.', 'slots': None, 'usage': 'fu %', 'word_id': 5, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_14 = {'position': 4, 'notes': None, 'body': '«testable», of testable properties.', 'slots': None, 'usage': 'nu %', 'word_id': 5, 'language': 'en', 'case_tags': '', 'grammar_code': 'a'}
definition_15 = {'position': 1, 'notes': None, 'body': 'a combining form of {kakto}, «act».', 'slots': None, 'usage': '', 'word_id': 1, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definition_16 = {'position': 1, 'notes': None, 'body': 'a combining form of {kakto}, «act».', 'slots': None, 'usage': '', 'word_id': 3, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definition_17 = {'position': 1, 'notes': None, 'body': 'a combining form of {pruci}, «test».', 'slots': None, 'usage': '', 'word_id': 4, 'language': 'en', 'case_tags': '', 'grammar_code': 'af'}
definitions = [definition_1, definition_2, definition_3, definition_4, definition_5, definition_6, definition_7, definition_8, definition_9, definition_10, definition_11, definition_12, definition_13, definition_14, definition_15, definition_16, definition_17]


# ===== CONNECTIONS ============================================================
connect_authors = [(1, 1), (1, 2), (1, 3), (2, 4), (2, 5), (1, 6), (2, 6)]  # (AID, WID)
connect_keys = [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (2, 5), (7, 6), (8, 6), (9, 7), (10, 8), (7, 9), (11, 10), (6, 11), (2, 11), (2, 12), (4, 13), (4, 14), (7, 15), (7, 16), (2, 17)]  # (KID, DID)
connect_words = [(2, 1), (2, 3), (2, 6), (5, 4), (5, 6)]  # (parent_id, child_id)


# EVENT 5 === appeared_words ===================================================
word_1_appeared_event_5 = {'notes': {'year': "(to '15)"}, 'tid_old': None, 'id_old': 10091, 'name': 'cii', 'type_id': 17, 'origin': '', 'event_start_id': 5, 'origin_x': '', 'event_end_id': None, 'match': '', 'rank': '', 'year': datetime.date(2013, 1, 1)}
word_2_appeared_event_5 = {'notes': {'year': "(to '15)"}, 'tid_old': None, 'id_old': 10098, 'name': 'flekukfoa', 'type_id': 6, 'origin': 'fle(ti)+kuk(ra)+fo(rm)a', 'event_start_id': 5, 'origin_x': 'flying quick form', 'event_end_id': None, 'match': '', 'rank': '', 'year': datetime.date(2008, 1, 1)}
word_3_appeared_event_5 = {'notes': {'year': "(to '15)"}, 'tid_old': None, 'id_old': 10099, 'name': 'lekveo', 'type_id': 5, 'origin': 'le(n)k(i)+ve(sl)o', 'event_start_id': 5, 'origin_x': 'electricity vessel', 'event_end_id': None, 'match': '', 'rank': '', 'year': datetime.date(2008, 1, 1)}
words_appeared = [word_1_appeared_event_5, word_2_appeared_event_5, word_3_appeared_event_5]

# EVENT 5 === deprecated_words =================================================
word_1_deprecated_event_5 = {'notes': {'year': "(fixed bad joint '16)"}, 'tid_old': None, 'id_old': 6637, 'name': 'osmio', 'type_id': 8, 'origin': 'ISV', 'event_start_id': 1, 'origin_x': '', 'event_end_id': 5, 'match': '', 'rank': '7+', 'year': datetime.date(1988, 1, 1)}
word_2_deprecated_event_5 = {'notes': {'year': "(corrected CV to CVh '16)"}, 'tid_old': None, 'id_old': 7668, 'name': 'riyhasgru', 'type_id': 5, 'origin': 'rih+y+has(fa)+gru(pa)', 'event_start_id': 1, 'origin_x': 'few house group', 'event_end_id': 5, 'match': '', 'rank': '7+', 'year': datetime.date(1999, 1, 1)}
word_3_deprecated_event_5 = {'notes': {'year': "(corrected CV to CVh '16)"}, 'tid_old': None, 'id_old': 7669, 'name': 'riyvei', 'type_id': 4, 'origin': 'rih+y+ve(tc)i', 'event_start_id': 1, 'origin_x': 'several events', 'event_end_id': 5, 'match': '', 'rank': '7+', 'year': datetime.date(1999, 1, 1)}
word_4_deprecated_event_5 = {'notes': {'year': "(fixed '16)"}, 'tid_old': None, 'id_old': 9036, 'name': 'testuda', 'type_id': 8, 'origin': 'Lin. Testudines', 'event_start_id': 1, 'origin_x': '', 'event_end_id': 5, 'match': '', 'rank': '7+', 'year': datetime.date(1997, 1, 1)}
words_deprecated = [word_1_deprecated_event_5, word_2_deprecated_event_5, word_3_deprecated_event_5, word_4_deprecated_event_5]

changed_words = words_appeared + words_deprecated

# ===== ALL EVENTS =================================================================
event_1 = {'annotation': 'Initial', 'name': 'Start', 'suffix': 'INIT', 'definition': 'The initial vocabulary before updates.', 'date': datetime.date(1975, 1, 1), }
event_2 = {'annotation': 'Syllables', 'name': '94/2', 'suffix': 'SC', 'definition': "Any 3+ syllable Complex that is CVC initial AND the C/C is a permissible initial must be 'y' hyphenated. The Slinkui test is vacated, and Tosmabru is replaced by this. Eg: 'paslinkui' -> 'pasylinkui' while the currently prohibitted '*tosmabru' -> 'tosymabru'.", 'date': datetime.date(1994, 1, 2), }
event_3 = {'annotation': 'Doubled Vowels', 'name': 'No double vowels in borrowings', 'suffix': 'DV', 'definition': "Doubled vowels (which require one to be stressed) are prohibited from Borrowings so they can be attached to Complexes without problems. Only 'alkooli' -> 'alkoholi' is affected.", 'date': datetime.date(2013, 1, 1), }
event_4 = {'annotation': 'Randall Trial', 'name': 'Randall Trial Words 1', 'suffix': 'RH1', 'definition': 'Randall Holmes trial words plus grammar vocab', 'date': datetime.date(2013, 12, 18), }
event_5 = {'annotation': 'Randall Cleanup', 'name': 'Randall Dictionary Cleanup', 'suffix': 'RDC', 'definition': 'parsed all the words in the dictionary, identified ones that the parser did not recognize as words', 'date': datetime.date(2016, 1, 15), }
event_6 = {'annotation': 'Torrua Repair', 'name': 'Torrua Dictionary Repair', 'suffix': 'TDR', 'definition': 'Repair of the dictionary by Torrua and Peter Hill', 'date': datetime.date(2019, 5, 25), }
events = [event_1, event_2, event_3, event_4, event_5, event_6]

# ===== SETTINGS ===============================================================
setting_1 = {'last_word_id': 10141, 'db_version': 2, 'db_release': '4.5.9', 'date': datetime.datetime(2020, 10, 9, 9, 10, 20)}
settings = [setting_1]

# ===== SYLLABLES ==============================================================
syllable_35 = {'allowed': True, 'name': 'vr', 'type': 'InitialCC'}
syllable_36 = {'allowed': True, 'name': 'zb', 'type': 'InitialCC'}
syllable_37 = {'allowed': True, 'name': 'zv', 'type': 'InitialCC'}
syllable_38 = {'allowed': False, 'name': 'cdz', 'type': 'UnintelligibleCCC'}
syllable_39 = {'allowed': False, 'name': 'cvl', 'type': 'UnintelligibleCCC'}
syllable_40 = {'allowed': False, 'name': 'ndj', 'type': 'UnintelligibleCCC'}
syllables = [syllable_35, syllable_36, syllable_37, syllable_38, syllable_39, syllable_40, ]

# ===== WORD SOURCES ===========================================================
word_source_1 = "2/3E act"
word_source_2 = "3/3F acte"
word_source_3 = "2/4C"
word_source_4 = "4/S"
word_sources = [word_source_1, word_source_2, word_source_3, word_source_4, ]

# ===== OTHER ITEMS ===========================================================
other_word_1 = {'tid_old': None, 'name': 'cirdui', 'origin': 'cir(na)+du(vr)i', 'type_id': 5, 'origin_x': 'learn discover', 'event_start_id': 1, 'match': '', 'event_end_id': None, 'rank': '7+', 'year': datetime.date(1991, 1, 1), 'notes': None, 'id': 1006, 'id_old': 992}
other_word_2 = {'notes': None, 'id': 2, 'tid_old': None, 'id_old': 3880, 'name': 'kakto', 'type_id': 9, 'origin': 'R akt | 4/4S | 3/3F acte | 2/3E act | 2/3H kam', 'event_start_id': 1, 'origin_x': '', 'event_end_id': None, 'match': '56%', 'created': datetime.datetime(2020, 10, 25, 7, 53, 54, 873132), 'rank': '1.0', 'year': datetime.date(1975, 1, 1)}
other_author_1 = {'full_name': 'Robert McIvor', 'id': 36, 'notes': '', 'abbreviation': 'RAM'}

all_objects = [(Key, keys), (Event, events), (Author, authors), (Type, types), (Word, words), (Definition, definitions)]
