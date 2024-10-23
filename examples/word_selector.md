# WordSelector — Example 1

The `WordSelector` class in `loglan_core\addons\word_selector.py` is used to construct complex queries to select words from a database. Here's an example usage of this class:

```python
# Import the WordSelector class
from loglan_core.addons.word_selector import WordSelector
```

## WordSelector Initialization
When creating `WordSelector` object, several parameters can be used:
- `model`: class of the words to be filtered (`BaseWord` by default). It is used to return words by associated class. 
> The specified class must inherit from `BaseWord`, otherwise a `ValueError` exception will be raised if the `disable_model_check` option is `False`. 
- `is_sqlite`: boolean that indicates whether the underlying database is SQLite. If `True`, the `WordSelector` will use SQLite-compatible SQL syntax.
> You must explicitly specify `is_sqlite` option when working with SQLite in order for case-sensitive search features to work correctly.
- `case_sensitive`: boolean that indicates whether the search is case-sensitive. If `True`, the `WordSelector` will use case-sensitive search in the underlying database.


- `disable_model_check`: boolean that indicates whether the `WordSelector` should perform a model check. If `True`, the `WordSelector` will not perform a model check.

## Create WordSelector instance
The simplest way to create a `WordSelector` object is to use the `WordSelector` constructor:

```python
ws = WordSelector()
```
By this way, we create a new `WordSelector` instance that will select **all words** from database.

## Apply Filters
Also, we can apply filters to our query.
For example, to select words associated with a specific event, use the `by_event` method:
```python
ws_event = WordSelector().by_event(event_id=1)
```

For filtering words by a specific name, use the `by_name` method:
```python
ws_by_name = WordSelector().by_name(name='proga')
```

Similarly, we can filter words by a specific key using the `by_key` method:

```python
ws_by_key = WordSelector().by_key(key='program')
```
Or use the `by_type` method for filtering words by a specific type:
```python
ws_by_type = WordSelector().by_type("Afx")
```

All these methods return a new instance of WordSelector with the filter applied.

We can also combine all these filters together:
```python
ws_combined = WordSelector().by_event(event_id=1).by_name(name='proga')
```
This will select words that are associated with the specified event AND have the specified name.

## Get Derivatives
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
These methods return a list of Word Objects or a single Word Object that match the applied filters.