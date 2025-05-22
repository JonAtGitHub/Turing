
class TuringMachineWatcher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TuringMachineWatcher, cls).__new__(cls)
        return cls._instance

    def _print_tape(self, operation):
        h = (" " * self._head_position) + "v"
        print ("{0}: {1}".format(operation, h))
        print ("{0}: {1}".format(operation, self._tape_contents))

    def tape_initialized(self, tape_contents, head_position):
        self._head_position = head_position
        self._tape_contents = tape_contents
        self._print_tape("I")

    def extend_tape(self, tape_contents, head_position):
        self._head_position = head_position
        self._tape_contents = tape_contents
        self._print_tape("X")

    def move_head(self, head_position):
        self._head_position = head_position
        self._print_tape("M")

    def tape_write(self, tape_contents):
        self._tape_contents = tape_contents
        self._print_tape("W")

    def step_start(self):
        pass

    def step_complete(self, is_final):
        if is_final: print ("FINAL")

    def step_input(self, state_input):
        self._state_input = state_input

    def step_transition(self, state_transition):
        print (str(self._state_input) + " : " + str(state_transition))

class Tape:

    def __init__(self, tape_alphabet_symbols="", blank_symbol = " ", input_symbols="", tape_contents="", head_position=0):
        if type(tape_alphabet_symbols) is not str: raise ValueError("'tape_alphabet_symbols' must be a string")
        alpha = set(tape_alphabet_symbols)
        if len(alpha) == 0: raise ValueError("Tape alphabet is empty")
        if len(alpha) != len(tape_alphabet_symbols): raise ValueError("Duplicate tape alphabet symbol(s) found")

        if type(blank_symbol) is not str: raise ValueError("'blank_symbol' must be a string")
        if len(blank_symbol) != 1: raise ValueError("Blank symbol must be single symbol")
        if blank_symbol not in alpha: raise ValueError("Blank symbol missing from tape alphabet symbols")

        if type(input_symbols) is not str: raise ValueError("'input_symbols' must be a string")
        input = set(input_symbols)
        if len(input) == 0: raise ValueError("Empty input symbols")
        if blank_symbol in input: raise ValueError("Blank symbol found in input symbols")
        if not alpha.issuperset(input): raise ValueError("Input symbol(s) missing from tape alphabet")

        if type(head_position) is not int: raise ValueError("Head position must be an integer")
        if head_position < 0: raise ValueError("Head position is outside of tape")

        if type(tape_contents) is not str: raise ValueError("'tape_contents' must be a string")
        tape = set(tape_contents)
        if len(tape) == 0: raise ValueError("Empty tape")
        if not alpha.issuperset(tape): raise ValueError("Input symbol(s) missing from tape contents")
        if head_position >= len(tape_contents): raise ValueError("Head position is outside of tape")

        self.__tape_alphabet_symbols = alpha
        self.__blank_symbol = blank_symbol
        self.__input_symbols = input
        self.__tape_contents = list(tape_contents)
        self.__head_position = head_position

        TuringMachineWatcher().tape_initialized(self.__stringify(), self.__head_position)

    def __stringify(self):
        return "".join(self.__tape_contents)

    def read(self):
        return self.__tape_contents[self.__head_position]

    def write_and_move(self, symbol, direction):
        if symbol not in self.__input_symbols: raise ValueError("Unknown write symbol")
        if direction not in "LR": raise ValueError("Invalid direction")
        self.__tape_contents[self.__head_position] = symbol
        TuringMachineWatcher().tape_write(self.__stringify())
        if direction == "L":
            if self.__head_position > 0:
                self.__head_position -= 1
                TuringMachineWatcher().move_head(self.__head_position)
            else:
                self.__tape_contents.insert(0, self.__blank_symbol)
                TuringMachineWatcher().extend_tape(self.__stringify(), self.__head_position)
        else: #if direction == "R":
            self.__head_position += 1
            if self.__head_position >= len(self.__tape_contents):
                self.__tape_contents.append(self.__blank_symbol)
                TuringMachineWatcher().extend_tape(self.__stringify(), self.__head_position)
            else:
                TuringMachineWatcher().move_head(self.__head_position)

class TuringMachine:

    def __init__(self, tape, states, transition_function, initial_state, final_states):

        if type(tape) is not Tape: raise ValueError("'tape' must be instance of Tape")

        if type(states) is not str: raise ValueError("'states' must be a string")
        _states = set(states)
        if len(_states) == 0 or len(_states) != len(states): raise ValueError("Empty or duplicate states")

        if type(initial_state) is not str or len(initial_state) != 1: raise ValueError("'initial_state' must be a string of length 1")
        if initial_state not in _states: raise ValueError("'initial_state' not found in 'states'")

        if type(final_states) is not str or len(final_states) == 0: raise ValueError("'final_states' must be a string of length 1 or greater")
        _final_states = set(final_states)
        if not _states.issuperset(_final_states): raise ValueError("One or more 'final_states' not found in 'states'")

        self.__tape = tape
        self.__states = _states
        self.__current_state = initial_state
        self.__final_states = _final_states
        self.__transition_function = transition_function # validate!

    def is_final(self):
        return self.__current_state in self.__final_states

    def step(self):
        if self.is_final(): return
        TuringMachineWatcher().step_start()
        rd = self.__tape.read()
        key = (self.__current_state, rd)
        if key not in self.__transition_function: raise ValueError("No transition rule for current state+input symbol " + str(key))
        TuringMachineWatcher().step_input(key)
        val = self.__transition_function[key]
        if val[2] not in self.__states: raise ValueError("Invalid next state in transition " + str(key) + " -> " + str(val))
        TuringMachineWatcher().step_transition(val)
        self.__tape.write_and_move(val[0], val[1])
        self.__current_state = val[2]
        TuringMachineWatcher().step_complete(self.is_final())

def inspect_transitions(transition_function):
    states = set()
    input_symbols = set()
    for k, v in transition_function.items():
        states.add(k[0])
        input_symbols.add(k[1])
        input_symbols.add(v[0])
        states.add(v[2])
    return ("".join(sorted(states)), "".join(sorted(input_symbols)))

def main():
    tape_alphabet_symbols = "01"
    blank_symbol = "0"
    input_symbols = "1"
    initial_tape = "000000000"; head_position = 4
    initial_tape = "0"; head_position = 0
    initial_state = "A"
    states = "ABCH"
    final_states = "H"
    transition_function = {
        # (current state, read symbol): (write symbol, head direction, next state)
        # 3 state busy beaver
        ("A", "0"): ("1", "R", "B"),
        ("A", "1"): ("1", "L", "C"),
        ("B", "0"): ("1", "L", "A"),
        ("B", "1"): ("1", "R", "B"),
        ("C", "0"): ("1", "L", "B"),
        ("C", "1"): ("1", "R", "H"),
    }

    inspection_results = inspect_transitions(transition_function)

    tape = Tape(tape_alphabet_symbols, blank_symbol, input_symbols, initial_tape, head_position)

    turing_machine = TuringMachine(tape, states, transition_function, initial_state, final_states)

    while not turing_machine.is_final():
        turing_machine.step()

if __name__ == "__main__":
    main()
