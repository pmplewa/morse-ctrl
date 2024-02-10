import logging

import attrs.validators as val
from attrs import Attribute, define, field
from mido import Message, open_output
from mido.ports import BaseOutput

from .utils import SETTERS

LOGGER = logging.getLogger(__name__)


@define
class Device:
    port: BaseOutput = field(
        converter=lambda value: open_output(value) if isinstance(value, str) else value,
        validator=val.instance_of(BaseOutput),
    )
    channel: int = field(
        default=0,
        validator=val.and_(val.instance_of(int), val.ge(0), val.le(15)),
    )


def _change_program(
    instance: Device, _attrib: Attribute, value: int | None
) -> int | None:
    if value is not None:
        msg = Message(
            type="program_change",
            channel=instance.channel,
            program=value,
        )
        LOGGER.info(msg)
        instance.port.send(msg)
    return value


@define
class ProgramDevice(Device):
    program: int | None = field(
        default=None,
        on_setattr=[*SETTERS, _change_program],
        validator=val.optional(val.and_(val.instance_of(int), val.ge(0), val.le(127))),
    )
