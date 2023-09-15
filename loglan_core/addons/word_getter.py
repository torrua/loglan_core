# -*- coding: utf-8 -*-
"""
This module contains an addon for basic Word Model,
which makes it possible to get words by event, name or key
"""
from typing import Union

from sqlalchemy import or_
from sqlalchemy.orm import Session
from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.key import BaseKey


class AddonWordGetter:
    """AddonWordGetter model"""

    @classmethod
    def by_event(
            cls, session: Session, event_id: int = None,
            add_to=None):
        """Query filtered by specified Event (the latest by default)

        Args:
          session:
          event_id: Union[BaseEvent, int]: Event object or Event.id (int) (Default value = None)
          add_to:
        Returns:
        """
        if not event_id:
            event_id = BaseEvent.latest(session).id

        request = add_to if add_to else session.query(cls)
        return cls._filter_event(event_id, request).order_by(cls.name)

    @classmethod
    def _filter_event(cls, event_id: int, add_to):
        return add_to.filter(cls.event_start_id <= event_id) \
            .filter(or_(cls.event_end_id > event_id, cls.event_end_id.is_(None)))

    @classmethod
    def by_name(
            cls, session: Session,
            name: str, event_id: Union[BaseEvent, int] = None,
            case_sensitive: bool = False, add_to=None):
        """Word.Query filtered by specified name

        Args:
          session:
          event_id:
          name: str:
          case_sensitive: bool:  (Default value = False)
          add_to:
        Returns:
        """

        request = add_to if add_to else session.query(cls)
        name = name.replace("*", "%")
        return cls.by_event(session, event_id, request).filter(
            cls.name.like(name) if case_sensitive else cls.name.ilike(name)
        )

    @classmethod
    def by_key(cls, session: Session,
               key: Union[BaseKey, str],
               language: str = None,
               event_id: Union[BaseEvent, int] = None,
               case_sensitive: bool = False, add_to=None):
        """Word.Query filtered by specified key

        Args:
          session:
          key: Union[BaseKey, str]:
          language: str: Language of key (Default value = None)
          event_id: Union[BaseEvent, int]:  (Default value = None)
          case_sensitive: bool:  (Default value = False)
          add_to:
        Returns:
        """

        request = add_to if add_to else session.query(cls)
        request = cls.by_event(session, event_id, request)

        key = (BaseKey.word if isinstance(key, BaseKey) else str(key)).replace("*", "%")
        request = request.join(BaseDefinition).join(t_connect_keys).join(BaseKey).filter(
            BaseKey.word.like(key) if case_sensitive else BaseKey.word.ilike(key))

        if language:
            request = request.filter(BaseKey.language == language)

        return request.order_by(cls.name)
