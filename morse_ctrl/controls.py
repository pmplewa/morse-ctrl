import logging
from enum import Enum
from functools import partial

import attrs.validators as val
from attrs import Attribute, field, setters
from mido import Message

from .devices import Device

LOGGER = logging.getLogger(__name__)

Metadata = dict[Enum, tuple[int, int]]


def _change_continous_control(
    instance: Device, _attrib: Attribute, value: int | None, *, control: int
) -> int | None:
    if value is not None:
        msg = Message(
            type="control_change",
            channel=instance.channel,
            control=control,
            value=value,
        )
        LOGGER.info(msg)
        instance.port.send(msg)
    return value


def _change_bool_control(
    instance: Device, attrib: Attribute, value: bool | None, **kwargs
) -> bool | None:
    if value is not None:
        _change_continous_control(instance, attrib, 127 if value else 0, **kwargs)
    return value


def _change_categorical_control(
    instance: Device, attrib: Attribute, value: Enum | None, **kwargs
) -> Enum | None:
    if value is not None:
        _change_continous_control(instance, attrib, attrib.metadata[value][0], **kwargs)
    return value


def create_continous_control(control: int):
    return field(
        default=None,
        on_setattr=[
            setters.convert,
            setters.validate,
            partial(_change_continous_control, control=control),
        ],
        converter=lambda value: round(12.7 * value) if value is not None else None,
        validator=val.optional(val.and_(val.instance_of(int), val.ge(0), val.le(127))),
    )


def create_bool_control(control: int):
    return field(
        default=None,
        on_setattr=[
            setters.validate,
            partial(_change_bool_control, control=control),
        ],
        validator=val.optional(val.instance_of(bool)),
    )


def create_categorical_control(control: int, metadata: Metadata):
    return field(
        default=None,
        metadata=metadata,
        on_setattr=[
            setters.validate,
            partial(_change_categorical_control, control=control),
        ],
        validator=val.optional(val.instance_of(Enum)),
    )
