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


class Amp(Enum):
    Fullerton = "Fullerton"
    London = "London"
    Dartford = "Dartford"


class Cab(Enum):
    Front_A = "Front_A"
    Front_B = "Front_B"
    Front_C = "Front_C"
    Back_A = "Back_A"
    Back_B = "Back_B"
    Back_C = "Back_C"


class LR(Enum):
    Left = "Left"
    Middle = "Middle"
    Right = "Right"


AMP_METADATA: Final[Metadata] = {
    Amp.Fullerton: (0, 42),
    Amp.London: (43, 85),
    Amp.Dartford: (86, 127),
}

CAB_METADATA: Final[Metadata] = {
    Cab.Front_A: (0, 20),
    Cab.Front_B: (22, 42),
    Cab.Front_C: (44, 64),
    Cab.Back_A: (66, 86),
    Cab.Back_B: (88, 108),
    Cab.Back_C: (110, 127),
}

LR_METADATA: Final[Metadata] = {
    LR.Left: (0, 42),
    LR.Middle: (43, 85),
    LR.Right: (86, 127),
}

DEFAULT_CAB: Final[dict[Amp, Cab]] = {
    Amp.Fullerton: Cab.Front_A,
    Amp.London: Cab.Front_B,
    Amp.Dartford: Cab.Front_C,
}


@define
class ACS1(ProgramDevice):
    bass = create_continous_control(3)
    mid = create_continous_control(14)
    treble = create_continous_control(15)

    volume = create_continous_control(20)
    gain = create_continous_control(21)
    room = create_continous_control(22)

    cab = create_categorical_control(27, CAB_METADATA)
    lr = create_categorical_control(28, LR_METADATA)
    amp = create_categorical_control(29, AMP_METADATA)

    bypass = create_bool_control(30)
    boost = create_bool_control(31)

    def set_eq(
        self, bass: float | None = 5, mid: float | None = 5, treble: float | None = 5
    ) -> Self:
        self.bass = bass
        self.mid = mid
        self.treble = treble
        return self

    def set_tone(
        self, volume: float | None = 6, gain: float | None = 6, room: float | None = 2
    ) -> Self:
        self.volume = volume
        self.gain = gain
        self.room = room
        return self

    def set_amp(
        self, amp: Amp, cab: Cab | None = None, lr: LR | None = LR.Middle
    ) -> Self:
        self.lr = lr
        self.amp = amp
        self.cab = cab or DEFAULT_CAB[amp]
        return self

    def enable(self) -> Self:
        self.bypass = False
        return self

    def disable(self) -> Self:
        self.bypass = True
        return self
