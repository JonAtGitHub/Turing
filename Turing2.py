
class Tape:

    def __init__(self, tape_alphabet_symbols="", blank_symbol = " ", input_symbols="", tape_contents="", head_position=0):
        alpha = set(tape_alphabet_symbols)
        if len(alpha) == 0: raise ValueError("Tape alphabet is empty")
        if len(alpha) != len(tape_alphabet_symbols): raise ValueError("Duplicate tape alphabet symbol(s) found")

        if len(blank_symbol) != 1: raise ValueError("Blank symbol must be single symbol")
        if blank_symbol not in alpha: raise ValueError("Blank symbol missing from tape alphabet symbols")

        input = set(input_symbols)
        if len(input) == 0: raise ValueError("Input symbols missing")
        if blank_symbol in input: raise ValueError("Blank symbol found in input symbols")
        if not alpha.issuperset(input): raise ValueError("Input symbol(s) missing from tape alphabet")

        if tape_contents == "": tape_contents = blank_symbol
        tape = set(tape_contents)
        if len(tape) == 0: raise ValueError("Empty tape")
        if not alpha.issuperset(tape): raise ValueError("Input symbol(s) missing from tape contents")

        if head_position < 0 or head_position >= len(tape_contents): raise ValueError("Head position is outside of tape")

        self.__tape_alphabet_symbols = alpha
        self.__blank_symbol = blank_symbol
        self.__input_symbols = input
        self.__tape_contents = list(tape_contents)
        self.__head_position = head_position

    def __str__(self):
        t = "".join(self.__tape_contents)
        h = (" " * self.__head_position) + "v"
        s = "{0}\n{1}".format(h, t)
        return s

    def read(self):
        return self.__tape_contents[self.__head_position]

    def write_and_move(self, symbol, direction):
        if symbol not in self.__input_symbols: raise ValueError("Unknown write symbol")
        if direction not in "LR": raise ValueError("Invalid direction")
        self.__tape_contents[self.__head_position] = symbol
        if direction == "L":
            if self.__head_position > 0:
                self.__head_position -= 1
            else:
                self.__tape_contents.insert(0, self.__blank_symbol)
        else: #if direction == "R":
            self.__head_position += 1
            if self.__head_position >= len(self.__tape_contents): self.__tape_contents.append(self.__blank_symbol)

class TuringMachine:

    def __init__(self, states, tape_alphabet_symbols, blank_symbol, input_symbols, transition_function, initial_state, final_states):
        _tape = Tape(tape_alphabet_symbols, blank_symbol, input_symbols) # validates those parameters

        # validate rest of the parameters
        if type(states) is not str: raise ValueError("'states' must be a string")
        _states = set(states)
        if len(_states) == 0 or len(_states) != len(states): raise ValueError("Empty or duplicate states")

        if type(initial_state) is not str or len(initial_state) != 1: raise ValueError("'initial_state' must be a string of length 1")
        if initial_state not in _states: raise ValueError("'initial_state' not found in 'states'")

        if type(final_states) is not str or len(final_states) == 0: raise ValueError("'final_states' must be a string of length 1 or greater")
        _final_states = set(final_states)
        if not _states.issuperset(_final_states): raise ValueError("One or more 'final_states' not found in 'states'")

        self.__tape = _tape
        self.__states = _states
        self.__current_state = initial_state
        self.__final_states = _final_states
        self.__transition_function = transition_function # validate!

    def __str__(self):
        return str(self.__tape)
    
    def is_final(self):
        return self.__current_state in self.__final_states
    
    def step(self):
        if self.is_final(): return
        rd = self.__tape.read()
        key = (self.__current_state, rd)
        if key not in self.__transition_function: raise ValueError("No transition rule for current state+input symbol " + str(key))
        val = self.__transition_function[key]
        self.__tape.write_and_move(val[0], val[1])
        if val[2] not in self.__states: raise ValueError("Invalid next state in transition " + str(key) + " -> " + str(val))
        self.__current_state = val[2]

def main():
    tape_alphabet_symbols = "01"
    blank_symbol = "0"
    input_symbols = "1"
    tape_contents = "" # all blank
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
    turing_machine = TuringMachine(states, tape_alphabet_symbols, blank_symbol, input_symbols,
                                   transition_function, initial_state, final_states)
    print(turing_machine)
    while not turing_machine.is_final():
        turing_machine.step()
        print(turing_machine)

if __name__ == "__main__":
    main()
