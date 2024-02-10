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
    Chorus = "Chorus"
    Phaser = "Phaser"
    Trem = "Trem"
    Vibe = "Vibe"
    Rotary = "Rotary"
    Filter = "Filter"


class Shape(Enum):
    Sine = "Sine"
    Triangle = "Triangle"
    Square = "Square"


class Div(Enum):
    Quarter = "Quarter"
    QuarterTriplet = "QuarterTriplet"
    Eighth = "Eighth"


class Type(Enum):
    One = 1
    Two = 2
    Three = 3


PROG_METADATA: Final[Metadata] = {
    Prog.Chorus: (0, 0),
    Prog.Phaser: (1, 1),
    Prog.Trem: (2, 2),
    Prog.Vibe: (3, 3),
    Prog.Rotary: (4, 4),
    Prog.Filter: (5, 5),
}

SHAPE_METADATA: Final[Metadata] = {
    Shape.Sine: (0, 0),
    Shape.Triangle: (1, 1),
    Shape.Square: (2, 2),
}

DIV_METADATA: Final[Metadata] = {
    Div.Quarter: (0, 0),
    Div.QuarterTriplet: (1, 1),
    Div.Eighth: (2, 2),
}

TYPE_METADATA: Final[Metadata] = {
    Type.One: (0, 0),
    Type.Two: (1, 1),
    Type.Three: (2, 2),
}


@define
class M1(ProgramDevice):
    rate = create_continous_control(3)
    depth = create_continous_control(9)
    lo_fi = create_continous_control(14)

    prog = create_categorical_control(18, PROG_METADATA)

    shape = create_categorical_control(15, SHAPE_METADATA)
    div = create_categorical_control(16, DIV_METADATA)
    type = create_categorical_control(17, TYPE_METADATA)

    env = create_continous_control(22)
    drive = create_continous_control(23)
    space = create_continous_control(24)

    tone = create_continous_control(19)
    sym = create_continous_control(20)
    x = create_continous_control(21)

    age = create_continous_control(25)
    noise = create_continous_control(26)
    warble = create_continous_control(27)

    rotary_speed = create_continous_control(86)
    skip = create_bool_control(87)

    bypass = create_bool_control(31)
    clock_bypass = create_bool_control(89)

    _tap = create_bool_control(85)

    def tap(self) -> Self:
        self._tap = True
        return self

    def enable(self) -> Self:
        self.bypass = False
        return self

    def disable(self) -> Self:
        self.bypass = True
        return self
