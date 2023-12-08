## Requirements
Loglan-Core is only a __data model__, a wrapper, and does not contain the dictionary data itself.
To work with a dictionary as an ORM, you need to set up your own database locally or remotely.

You can connect it as follows:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URI = os.environ.get('LOD_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine, future=True))
session = Session()
```
where `LOD_DATABASE_URL` is the database URI starting with `postgresql://***`.

Next, we will use the resulting instance of the `Session` class to retrieve data from the database and work with it.

## Example 1 - Loglan Word
Let's look at the definition of the word "proga" from the LOD dictionary.

&nbsp;&nbsp;&nbsp;&nbsp;__proga__,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<font color="green">_pog <Int.>_</font> I-Prim SLR '93 7+<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(4n) B is a <font color="blue">_program_</font> for/to do P on system F written by K. [B-PFK]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Used in: fanpogsea; pogdai; pogleu; pogmai; pogmao; pognakso; pogpai; pogsea; selkopyproga;

### Retrieving an object
First we need to get the Word object.
This can be done using `by_name` method of special class `WordSelector`. 
This method returns a statement for the database, which we execute using the `session` object.

```python
from loglan_core.addons.word_selector import WordSelector

request = WordSelector().by_name("proga")
word = session.execute(request).first()

print(word)
>>> <BaseWord ID **** proga>
```

Let's see what this object consists of:
```python
print(word.__dict__)
>>> {
        '_sa_instance_state': ***,
        'created': datetime.datetime(***),
        'updated': None,
        'id': ****,
        'id_old': 7166,
        'name': 'proga',
        'type_id': 11,
        'event_start_id': 1,
        'event_end_id': None,
        'tid_old': None,
        'origin': 'Int.',
        'origin_x': '', 
        'match': '',
        'rank': '7+',
        'year': datetime.date(1993, 1, 1),
        'notes': None,
}
```
### Retrieving additional data
Now we will get more information regarding this word.

#### Authors
_The author of a word is not necessarily one person and not even necessarily a person._

_This word has only one author, but there may be more in the list._
```python
print(word.authors)
>>> [
        BaseAuthor(
            abbreviation='SLR',
            full_name='Steve Rice',
            id=**,
            notes='',
        ),
    ]
```

#### Definitions
_This word has only one definition, but there may be more in the list._
```python
print(word.definitions)
>>> [
        BaseDefinition(
            body='B is a «program» for/to do P on system F written by K.',
            case_tags='B-PFK',
            grammar_code='n',
            id=****,
            language='en', 
            notes=None, 
            position=1, 
            slots=4, 
            usage='', 
            word_id=****,
        ),
    ]
```

#### Word's Type
_All words in Loglan are divided into three main types and several subtypes._
```python
print(word.type)
>>> <BaseType ID 11 I-Prim (Predicate)>
```

#### Lexical Events
_Events when a word appeared and when (and if) it was excluded from the lexicon._
```python
print(word.event_start)
>>> <BaseEvent ID 1 Start (1975-01-01)>

print(word.event_end)
>>> None
```

#### Keys
_Keys are keywords that define a word in a foreign language. They are taken from the definitions._

_This word has only one key, but there may be more in the list._

```python
print(word.keys)
>>> [
        BaseKey(
            id=****,
            language='en',
            word='program',
        ), 
    ]
```

#### Word's Derivatives
_This includes the so-called __“djifoa”__, that is, short forms of the word and complexes - 
derived words consisting of several djifoa. For example, the short form of the word __“proga”__ is __“pog”__. 
And __“pogleu”__ is a complex consisting of two parts - p(r)og(a)+le(ng)u - and means “programming language”._
```python
print(word.derivatives)
>>> [
        BaseWord(name='fanpogsea', origin='fan(ve)+p(r)og(a)+se(tf)a', origin_x='reverse program set', type_id=6, ...),
        BaseWord(name='pog', origin='p(r)og(a)', origin_x='', type_id=2, ...), 
        BaseWord(name='pogdai', origin='p(r)og(a)+da(nc)i', origin_x='program design', type_id=5, ...), 
        BaseWord(name='pogleu', origin='p(r)og(a)+le(ng)u', origin_x='program language', type_id=5, ...), 
        BaseWord(name='pogmai', origin='p(r)og(a)+ma(tc)i', origin_x='program(mable) machine', type_id=5, ...), 
        BaseWord(name='pogmao', origin='p(r)og(a)+ma(dz)o', origin_x='program make', type_id=5, ...), 
        BaseWord(name='pognakso', notes=None, origin='p(r)og(a)+nakso', origin_x='program fix', type_id=5, ...), 
        BaseWord(name='pogpai', origin='p(r)og(a)+pa(rt)i', origin_x='program part', type_id=5, ...), 
        BaseWord(name='pogsea', origin='p(r)og(a)+se(tf)a', origin_x='program set', type_id=5, ...), 
        BaseWord(name='selkopyproga', origin='sel(ji)+kop(ca)+y+proga', origin_x='self copy program', type_id=6, ...),
    ]
```

#### Finally
Thus, we received all the information about the word from the original entry in the dictionary.
