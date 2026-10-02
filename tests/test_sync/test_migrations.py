"""
Tests for Alembic migrations.
"""

import os
import tempfile
import pytest

pytest.importorskip("alembic")

from alembic.config import Config  # pylint: disable=wrong-import-position
from alembic import command  # pylint: disable=wrong-import-position
from sqlalchemy import create_engine, inspect  # pylint: disable=wrong-import-position


def test_alembic_upgrade_and_downgrade():
    """Verify that Alembic migrations run cleanly from base to head and back."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_mig.db").replace("\\", "/")
        cfg = Config()
        cfg.set_main_option("script_location", "alembic")
        cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

        # Upgrade to head
        command.upgrade(cfg, "head")

        engine = create_engine(f"sqlite:///{db_path}")
        inspector = inspect(engine)
        tables = set(inspector.get_table_names())
        expected_tables = {
            "authors",
            "events",
            "keys",
            "settings",
            "syllables",
            "types",
            "words",
            "connect_authors",
            "connect_words",
            "definitions",
            "connect_keys",
            "alembic_version",
        }
        assert expected_tables.issubset(tables)
        engine.dispose()

        # Downgrade to base
        command.downgrade(cfg, "base")

        engine2 = create_engine(f"sqlite:///{db_path}")
        tables_after = set(inspect(engine2).get_table_names())
        assert len(tables_after - {"alembic_version"}) == 0
        engine2.dispose()
