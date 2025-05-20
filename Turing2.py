from enum import Enum

Direction = Enum('Direction', names='LEFT RIGHT')

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

        tape = set(tape_contents)
        if len(tape) == 0: raise ValueError("Empty tape")
        if not alpha.issuperset(tape): raise ValueError("Input symbol(s) missing from tape contents")

        if head_position < 0 or head_position >= len(tape_contents): raise ValueError("Head position is outside of tape")

        self.__tape_alphabet_symbols = alpha
        self.__blank_symbol = blank_symbol
        self.__input_symbols = input
        self.__tape_contents = list(tape_contents)
        self.__head_position = head_position

    def read(self):
        return self.__tape_contents[self.__head_position]

    def write_and_move(self, symbol, direction):
        if symbol not in self.__input_symbols: raise ValueError("Unknown write symbol")
        self.__tape_contents[self.__head_position] = symbol
        if direction == Direction.LEFT:
            if self.__head_position > 0:
                self.__head_position -= 1
            else:
                self.__tape_contents.insert(0, self.__blank_symbol)
        else:
            self.__head_position += 1
            if self.__head_position >= len(self.__tape_contents): self.__tape_contents.append(self.__blank_symbol)
