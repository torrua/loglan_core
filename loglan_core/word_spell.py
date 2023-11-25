# -*- coding: utf-8 -*-
"""
This module contains a basic WordSpell Model
"""
from loglan_core.base import BaseModel
from loglan_core.table_names import T_NAME_WORD_SPELLS


class BaseWordSpell(BaseModel):
    """BaseWordSpell model"""

    __tablename__ = T_NAME_WORD_SPELLS
