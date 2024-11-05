import pytest
from loglan_core import Setting


@pytest.mark.usefixtures("db_session")
class TestSetting:

    def test_str(self, db_session):
        setting_1: Setting = db_session.query(Setting).filter(Setting.id == 1).first()
        assert str(setting_1) == '<BaseSetting ID 1 db version 2 (release 4.5.9)>'
