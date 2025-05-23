
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

#*********************************************************************
# from https://en.wikipedia.org/wiki/Turing_machine

@dataclass
class BusyBeaver(TuringMachineConfiguration):
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

_tm = BusyBeaver()
_configs[_tm.name] = _tm

@dataclass
class BusyBeaver2(BusyBeaver):
    name: str                   = "BusyBeaver2"
    initial_tape: str           = "0000000"
    head_position: int          = 3

_tm = BusyBeaver2()
_configs[_tm.name] = _tm

#*********************************************************************
# L = { 0^n1^n | n E N }
# from https://web.stanford.edu/class/archive/cs/cs103/cs103.1142/lectures/18/Small18.pdf

@dataclass
class Stanford0n1n(TuringMachineConfiguration):
    name: str                   = "Stanford0n1n"
    tape_alphabet_symbols: str  = "_01"
    blank_symbol: str           = "_"
    input_symbols: str          = "01"
    initial_tape: str           = "_0011_"
    head_position: int          = 1
    initial_state: str          = "0"
    final_states: str           = "AR"
    states: str                 = "0123AR"
    transition_function: dict   = field(default_factory=lambda: {
        ("0", "0"): ("_", "R", "1"),
        ("0", "1"): ("1", "R", "R"),
        ("0", "_"): ("_", "R", "A"),
        ("1", "0"): ("0", "R", "1"),
        ("1", "1"): ("1", "R", "1"),
        ("1", "_"): ("_", "L", "2"),
        ("2", "0"): ("0", "R", "R"),
        ("2", "1"): ("_", "L", "3"),
        ("2", "_"): ("_", "R", "R"),
        ("3", "0"): ("0", "L", "3"),
        ("3", "1"): ("1", "L", "3"),
        ("3", "_"): ("_", "R", "0"),
    })

_tm = Stanford0n1n()
_configs[_tm.name] = _tm

#*********************************************************************
# L = { 0^(2^n) | n >= 0 }
# from p3 https://ics.uci.edu/~goodrich/teach/cs162/notes/turing2.pdf

@dataclass
class Uci02n(TuringMachineConfiguration):
    name: str                   = "Uci02n"
    tape_alphabet_symbols: str  = "_0x"
    blank_symbol: str           = "_"
    input_symbols: str          = "0"
    initial_tape: str           = "000"
    head_position: int          = 0
    initial_state: str          = "1"
    final_states: str           = "AR"
    states: str                 = "12345AR"
    transition_function: dict   = field(default_factory=lambda: {
        ("1", "0"): ("_", "R", "2"),
        ("1", "x"): ("x", "R", "R"),
        ("1", "_"): ("_", "R", "R"),
        ("2", "0"): ("x", "R", "3"),
        ("2", "x"): ("x", "R", "2"),
        ("2", "_"): ("_", "R", "A"),
        ("3", "0"): ("0", "R", "4"),
        ("3", "x"): ("x", "R", "3"),
        ("3", "_"): ("_", "L", "5"),
        ("4", "0"): ("x", "R", "3"),
        ("4", "x"): ("x", "R", "4"),
        ("4", "_"): ("_", "R", "R"),
        ("5", "0"): ("0", "L", "5"),
        ("5", "x"): ("x", "L", "5"),
        ("5", "_"): ("_", "R", "2"),
    })

_tm = Uci02n()
_configs[_tm.name] = _tm

#*********************************************************************
# L = { w#w | w E {0, 1}* }
# from p10 https://ics.uci.edu/~goodrich/teach/cs162/notes/turing2.pdf

@dataclass
class wPoundw(TuringMachineConfiguration):
    name: str                   = "w#w"
    tape_alphabet_symbols: str  = "01#x_"
    blank_symbol: str           = "_"
    input_symbols: str          = "01#"
    initial_tape: str           = "01#10"
    head_position: int          = 0
    initial_state: str          = "1"
    final_states: str           = "AR"
    states: str                 = "12345687AR"
    transition_function: dict   = field(default_factory=lambda: {
        ("1", "0"): ("x", "R", "2"),
        ("1", "1"): ("x", "R", "3"),
        ("1", "#"): ("#", "R", "8"),
        ("1", "x"): ("x", "R", "R"),
        ("1", "_"): ("_", "R", "R"),
        ("2", "0"): ("0", "R", "2"),
        ("2", "1"): ("1", "R", "2"),
        ("2", "#"): ("#", "R", "4"),
        ("2", "x"): ("x", "R", "R"),
        ("2", "_"): ("_", "R", "R"),
        ("3", "0"): ("0", "R", "3"),
        ("3", "1"): ("1", "R", "3"),
        ("3", "#"): ("#", "R", "5"),
        ("3", "x"): ("x", "R", "R"),
        ("3", "_"): ("_", "R", "R"),
        ("4", "0"): ("x", "L", "6"),
        ("4", "1"): ("1", "R", "R"),
        ("4", "#"): ("#", "R", "R"),
        ("4", "x"): ("x", "R", "4"),
        ("4", "_"): ("_", "R", "R"),
        ("5", "0"): ("0", "R", "R"),
        ("5", "1"): ("x", "L", "6"),
        ("5", "#"): ("#", "R", "R"),
        ("5", "x"): ("x", "R", "5"),
        ("5", "_"): ("_", "R", "R"),
        ("6", "0"): ("0", "L", "6"),
        ("6", "1"): ("1", "L", "6"),
        ("6", "#"): ("#", "L", "7"),
        ("6", "x"): ("x", "L", "6"),
        ("6", "_"): ("_", "R", "R"),
        ("7", "0"): ("0", "L", "7"),
        ("7", "1"): ("1", "L", "7"),
        ("7", "#"): ("#", "R", "R"),
        ("7", "x"): ("x", "R", "1"),
        ("7", "_"): ("_", "R", "R"),
        ("8", "0"): ("0", "R", "R"),
        ("8", "1"): ("1", "R", "R"),
        ("8", "#"): ("#", "R", "R"),
        ("8", "x"): ("x", "R", "8"),
        ("8", "_"): ("_", "R", "A"),
    })

_tm = wPoundw()
_configs[_tm.name] = _tm

