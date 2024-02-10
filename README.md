# morse-ctrl

This package contains Python classes to control the Walrus Audio MAKO series
effect pedals via MIDI, using the `mido` library.

## Installation

To install the latest development version, run:

```bash
pip install git+https://github.com/pmplewa/morse-ctrl.git
```

## Examples

```python
import mido

from morse_ctrl.acs1 import ACS1, Amp


with mido.open_output() as port:
    acs = ACS1(port)

    # Recall the first preset:
    acs.program = 0

    # Set the volume knob (0...10):
    acs.volume = 5

    # Set all three EQ knobs at once:
    acs.set_eq(7, 5, 6)

    # Select the amplifier (as well as its default speaker cabinet):
    acs.set_amp(Amp.London)

    # Activat the boost switch:
    acs.boost = True
```
