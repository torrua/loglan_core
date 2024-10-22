# WordSelector — Example 1

The `WordSelector` class in `loglan_core\addons\word_selector.py` is used to construct complex queries to select words from a database. Here's an example usage of this class:

```python
# Import the WordSelector class
from loglan_core.addons.word_selector import WordSelector
```

## WordSelector Initialization
When creating `WordSelector` object, several variables can be used:
- `model`: This parameter specifies the class of the words to be filtered (`BaseWord` by default). It is used to filter words by their associated class. 
> The specified class must inherit from `BaseWord`, otherwise a `ValueError` exception will be raised if the `disable_model_check` option is `False`. 
- `is_sqlite`: This parameter is a boolean that indicates whether the underlying database is SQLite. If `True`, the `WordSelector` will use SQLite-compatible SQL syntax.
> You must explicitly specify `is_sqlite` option when working with SQLite in order for case-sensitive search features to work correctly.
- `case_sensitive`: This parameter is a boolean that indicates whether the search is case-sensitive. If `True`, the `WordSelector` will use case-sensitive search in the underlying database.


- `disable_model_check`: This parameter is a boolean that indicates whether the `WordSelector` should perform a model check. If `True`, the `WordSelector` will not perform a model check.
## WordSelector Variables
When manipulating a `WordSelector` object, several variables can be used:

- `event_id`: This variable represents the id of an event. It is used to filter words associated with a specific event.
- `name`: This variable represents the name of a word. It is used to filter words by a specific name.
- `key`: This variable represents the key of a word. It is used to filter words by a specific key.


## Create WordSelector instance

We can then use the methods provided by the class to apply filters to our query.
For example, to select words associated with a specific event, we use the `by_event` method:
```python
ws_event = WordSelector().by_event(event_id=1)
```

The `by_event` method returns a new instance of WordSelector with the filter applied.
We can also filter words by a specific name. We use the `by_name` method:
```python
ws_by_name = WordSelector().by_name(name='proga')
```
The `by_name` method, like `by_event`, also returns a new instance of WordSelector with the filter applied.
Similarly, we can filter words by a specific key using the `by_key` method:

```python
ws_by_key = WordSelector().by_key(key='program')
```
Or using the `by_type` method:
```python
ws_by_type = WordSelector().by_type("Afx")
```

We can also combine all these filters:
```python
ws_combined = WordSelector().by_event(event_id=1).by_name(name='proga')
```
This will select words that are associated with the specified event AND have the specified name.


Three methods are available for getting derivatives of the word by `word_id`:

`get_derivatives_of`, `get_complexes_of` and `get_affixes_of`

```python
ws_derivatives = WordSelector().get_derivatives_of(word_id=1)
ws_derivatives = WordSelector().get_complexes_of(word_id=1)
ws_derivatives = WordSelector().get_affixes_of(word_id=1)
```
You can combine them with filters as well.

## Get Results from WordSelector
The WordSelector object returns a classic SQLAlchemy `Select` Object, so we can use it as normal within a session, like this:
```python
all_words = session.scalars(ws_combined.get_statement()).all()
first_word = session.scalar(ws_combined.get_statement())
```
Also, we can use the internal `all`, `scalar` or `fetchmany` methods:
```python
all_words = ws_combined.all(session)
first_word = ws_combined.scalar(session)
first_five_words = ws_combined.fetchmany(session, size=5)
```
These methods will return a list of Word Objects or a single Word Object that match the applied filters.