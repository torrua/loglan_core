from loglan_core import (
    Author,
    Definition,
    Event,
    Key,
    Setting,
    Syllable,
    Type,
    Word,
    t_connect_words,
    t_connect_authors,
    t_connect_keys,
)

from tests.data import (
    words,
    changed_words,
    types,
    events,
    authors,
    definitions,
    keys,
    un_keys,
    syllables,
    settings,
    connect_words,
    connect_authors,
    connect_keys,
)


def get_objects():
    words_objects = [Word(**obj) for obj in words + changed_words]
    types_objects = [Type(**obj) for obj in types]
    events_objects = [Event(**obj) for obj in events]
    authors_objects = [Author(**obj) for obj in authors]
    definitions_objects = [Definition(**obj) for obj in definitions]
    keys_objects = [Key(**obj) for obj in keys + un_keys]
    syllables_objects = [Syllable(**obj) for obj in syllables]
    settings_objects = [Setting(**obj) for obj in settings]
    return (
        authors_objects,
        definitions_objects,
        events_objects,
        keys_objects,
        settings_objects,
        syllables_objects,
        types_objects,
        words_objects,
    )


def create_db(session):
    add_objects(session)
    link_objects(session)
    session.commit()


def link_objects(session):

    for parent_id, child_id in connect_words:
        ins = t_connect_words.insert().values(parent_id=parent_id, child_id=child_id)
        session.execute(ins)

    for author_id, word_id in connect_authors:
        ins = t_connect_authors.insert().values(AID=author_id, WID=word_id)
        session.execute(ins)

    for key_id, definition_id in connect_keys:
        ins = t_connect_keys.insert().values(KID=key_id, DID=definition_id)
        session.execute(ins)


def add_objects(session):
    objects = get_objects()
    for obj in objects:
        session.add_all(obj)
