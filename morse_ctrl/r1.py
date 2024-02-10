from contextlib import contextmanager
from copy import copy
from enum import Enum
from typing import Final

from attrs import define
from typing_extensions import Self

from .controls import (
    Metadata,
    create_bool_control,
    create_categorical_control,
    create_continous_control,
)
from .devices import ProgramDevice


class Prog(Enum):
    Spring = "Spring"
    Hall = "Hall"
    Plate = "Plate"
    BFR = "BFR"
    RFRCT = "RFRCT"
    Air = "Air"


PROG_METADATA: Final[Metadata] = {
    Prog.Spring: (1, 1),
    Prog.Hall: (2, 2),
    Prog.Plate: (3, 3),
    Prog.BFR: (4, 4),
    Prog.RFRCT: (5, 5),
    Prog.Air: (6, 6),
}


@define
class R1(ProgramDevice):
    decay = create_continous_control(3)
    swell = create_continous_control(14)
    mix = create_continous_control(15)

    prog = create_categorical_control(23, PROG_METADATA)

    rate = create_continous_control(20)
    depth = create_continous_control(21)
    pre_delay = create_continous_control(22)

    lo = create_continous_control(24)
    high = create_continous_control(25)
    x = create_continous_control(26)

    bypass = create_bool_control(30)
    sustain = create_bool_control(31)

    @contextmanager
    def sustained(self):
        instance = copy(self)
        try:
            instance.sustain = True
            yield instance
        finally:
            instance.sustain = False

    def enable(self) -> Self:
        self.bypass = False
        return self

    def disable(self) -> Self:
        self.bypass = True
        return self
