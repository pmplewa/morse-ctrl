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
    Dig = "Dig"
    Mod = "Mod"
    Vint = "Vint"
    Dual = "Dual"
    Rev = "Rev"


class Div(Enum):
    Quarter = "Quarter"
    Eighth = "Eighth"
    DottedEighth = "DottedEighth"


PROG_METADATA: Final[Metadata] = {
    Prog.Dig: (0, 0),
    Prog.Mod: (1, 1),
    Prog.Vint: (2, 2),
    Prog.Dual: (3, 3),
    Prog.Rev: (4, 4),
}


DIV_METADATA: Final[Metadata] = {
    Div.Quarter: (0, 42),
    Div.Eighth: (43, 85),
    Div.DottedEighth: (86, 127),
}


@define
class D1(ProgramDevice):
    time = create_continous_control(14)
    repeats = create_continous_control(15)
    mix = create_continous_control(20)

    prog = create_categorical_control(24, PROG_METADATA)
    attack = create_continous_control(25)

    mod = create_continous_control(21)
    tone = create_continous_control(22)
    age = create_continous_control(23)

    div = create_categorical_control(28, DIV_METADATA)

    bypass = create_bool_control(29)
    clock_bypass = create_bool_control(86)

    _tap = create_bool_control(30)

    def tap(self) -> Self:
        self._tap = True
        return self

    def enable(self) -> Self:
        self.bypass = False
        return self

    def disable(self) -> Self:
        self.bypass = True
        return self
