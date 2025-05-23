
from dataclasses import dataclass, field

@dataclass
class TuringMachineConfiguration:
    name: str
    tape_alphabet_symbols: str  # Gamma
    blank_symbol: str           # b
    input_symbols: str          # Sigma
    initial_tape: str
    head_position: int
    initial_state: str          # q0
    final_states: str           # F
    states: str                 # Q
    # (current state, read symbol): (write symbol, head direction, next state)
    transition_function: dict   # delta

_configs = {}

def get(name):
    if name not in _configs: raise ValueError("Configuration " + name + " not found")
    return _configs[name]

@dataclass
class BusyBeaverTuringMachine(TuringMachineConfiguration):
    name: str                   = "BusyBeaver"
    tape_alphabet_symbols: str  = "01"
    blank_symbol: str           = "0"
    input_symbols: str          = "1"
    initial_tape: str           = "0"
    head_position: int          = 0
    initial_state: str          = "A"
    final_states: str           = "H"
    states: str                 = "ABCH"
    transition_function: dict   = field(default_factory=lambda: {
        ("A", "0"): ("1", "R", "B"),
        ("A", "1"): ("1", "L", "C"),
        ("B", "0"): ("1", "L", "A"),
        ("B", "1"): ("1", "R", "B"),
        ("C", "0"): ("1", "L", "B"),
        ("C", "1"): ("1", "R", "H"),
    })

_busy_beaver = BusyBeaverTuringMachine()
_configs[_busy_beaver.name] = _busy_beaver

@dataclass
class BusyBeaver2TuringMachine(BusyBeaverTuringMachine):
    name: str                   = "BusyBeaver2"
    initial_tape: str           = "0000000"
    head_position: int          = 3

_busy_beaver2 = BusyBeaver2TuringMachine()
_configs[_busy_beaver2.name] = _busy_beaver2
