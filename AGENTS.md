# Loglan-Core — Agent Guide

## Project

SQLAlchemy database model for the Loglan constructed language dictionary. Single package.

## Commands

- `pytest --cov=loglan_core --cov-report=xml --cov-report=term` — run all tests with coverage
- `pytest tests/test_sync/` — synchronous SQLite tests only
- `pytest tests/test_async/` — async aiosqlite tests only
- `pylint --fail-under=9.5 loglan_core` — lint (must score >=9.5; CI enforces)
- `black --check --verbose ./loglan_core` — formatting check (CI enforces)
- `mypy loglan_core` — typecheck (available, not enforced in CI)

## Package structure

```
loglan_core/         # main package
├── base.py          # BaseModel (AsyncAttrs + DeclarativeBase)
├── word.py, author.py, definition.py, event.py, key.py,
│   type.py, setting.py, syllable.py, word_spell.py   # models
├── relationships.py # many-to-many association tables
├── addons/          # selectors, exporter, word linker/sourcer
└── service/         # annotated types (str_008..str_255) + table name constants
tests/
├── data.py          # shared test data dicts
├── objects.py       # shared factory functions (get_objects, create_db, add_objects)
├── test_sync/       # synchronous tests (SQLite in-memory)
└── test_async/      # async tests (aiosqlite)
```

Public API is exported from `loglan_core/__init__.py`. Import via `from loglan_core import Word, Base, WordSelector, ...`.

## Key conventions

- All models inherit `BaseModel(AsyncAttrs, DeclarativeBase)` from `base.py`
- String length annotations (`str_008`..`str_255`) are custom `Annotated` types mapped to `String(n)` via `type_annotation_map` in `BaseModel.registry`
- Model class-level `Mapped` columns AND explicit `__init__` with named parameters are both defined
- DB column names sometimes differ from attribute names (e.g. `tid_old` maps to `TID_old`, `type_id` maps to `type`)
- `Word.type` uses `lazy="joined"` (required for `affixes`/`complexes` hybrid properties to work)
- Association tables: `t_connect_authors`, `t_connect_words`, `t_connect_keys` (exported from `loglan_core`)

## Testing

- Test data is shared between sync and async suites via `tests/data.py` + `tests/objects.py`
- Sync: `@pytest.mark.usefixtures("db_session")` class decorator; each function gets a fresh SQLite in-memory DB
- Async: uses `pytest-asyncio` with `asyncio_mode = auto` and `asyncio_default_fixture_loop_scope = session` (configured in `pyproject.toml`)
- Both suites rebuild the schema and insert test fixtures per test function

## Gotchas

- `alembic.ini` and `main.py` are gitignored (contain credentials / local-only code)
- `.env` may contain real database credentials — do not commit changes
- `__init__.py` in `tests/` is required (enables `from ..objects import ...` in conftest)
- Only one Alembic migration exists (`07896d9fef5d_init_db.py`)
