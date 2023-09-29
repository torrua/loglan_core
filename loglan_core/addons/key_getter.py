# -*- coding: utf-8 -*-
"""

This module contains an addon for basic Key Model,
which makes it possible to get Key objects by event
"""

from typing import Union

from sqlalchemy import or_
from sqlalchemy.orm import Session
from loglan_core.connect_tables import t_connect_keys
from loglan_core.definition import BaseDefinition
from loglan_core.event import BaseEvent
from loglan_core.word import BaseWord

# TODO Rewrite as separate Class


class AddonKeyGetter:
    """AddonKeyGetter model"""

    @classmethod
    def by_event(
        cls,
        session: Session,
        event_id: BaseEvent | int | None = None,
        add_to=None,
    ):
        """Query filtered by specified Event (latest by default)

        Args:
          :param add_to:
          :param event_id: Union[BaseEvent, int]:
            Event object or Event.id (int) (Default value = None)
          :param session:
        Returns:
        """
        if not event_id:
            last_event = session.execute(BaseEvent.latest()).scalar()
            current_event_id = last_event.id if last_event else None
        else:
            current_event_id = (
                BaseEvent.id if isinstance(event_id, BaseEvent) else int(event_id)
            )

        request = add_to if add_to else session.query(cls)
        return cls._filter_event(current_event_id, request)

    @classmethod
    def _filter_event(cls, event_id: Union[BaseEvent, int], add_to):
        return (
            add_to.join(t_connect_keys)
            .join(BaseDefinition)
            .join(BaseWord)
            .filter(BaseWord.event_start_id <= event_id)
            .filter(
                or_(BaseWord.event_end_id > event_id, BaseWord.event_end_id.is_(None))
            )
        )
