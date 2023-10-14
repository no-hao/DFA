# *****************************************************************
# DFA Simulator
# Author: Eric sitne
#
# Description:
# This program provides a simulator for Deterministic Finite Automatons (DFAs).
# This simulator allows users to define DFAs in a specific file format and then
# test strings against these DFAs to determine acceptance or rejection.
# *****************************************************************

class State:
    """
    Represents a state in a Deterministic Finite Automaton (DFA).
    """
    
    # ***************************************************************
    # __init__
    # ***************************************************************
    # Purpose: Initialize a new State.
    def __init__(self, state_id, is_accepting, transitions):
        self.state_id = state_id
        self.is_accepting = is_accepting
        self.transitions = transitions


class DFALoader:
    """
    Utility class to load a DFA from a file.
    """
    
    # ***************************************************************
    # load_from_file
    # ***************************************************************
    # Purpose: Load a DFA from a given file.
    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            num_states = int(file.readline().strip())
            accepting_states = list(map(int, file.readline().split()))
            alphabet = file.readline().split()
            transitions = [list(map(int, file.readline().split())) for _ in range(num_states)]
            
        return DFA(num_states, accepting_states, alphabet, transitions)


class DFA:
    """
    Represents a Deterministic Finite Automaton (DFA).
    """
    
    # ***************************************************************
    # __init__
    # ***************************************************************
    # Purpose: Initialize a new DFA.
    def __init__(self, num_states, accepting_states, alphabet, transitions):
        self.states = [State(i, i in accepting_states, transitions[i]) for i in range(num_states)]
        self.alphabet = alphabet
        self.initial_state = self.states[0]
        self.current_state = self.initial_state

    # ***************************************************************
    # transition
    # ***************************************************************
    # Purpose: Transition to the next state based on the given input character.
    def transition(self, char):
        if char not in self.alphabet:
            raise ValueError(f"Invalid input character: {char}")
        next_state_idx = self.states.index(self.current_state)
        char_idx = self.alphabet.index(char)
        self.current_state = self.states[self.current_state.transitions[char_idx]]

    # ***************************************************************
    # simulate
    # ***************************************************************
    # Purpose: Simulate the DFA for a given input string.
    def simulate(self, input_string):
        self.reset()
        computation_trace = [(self.current_state.state_id, input_string)]

        for char in input_string:
            if char not in self.alphabet:
                computation_trace.append(("INVALID INPUT", ""))
                return computation_trace, "", "REJECTED"
            self.transition(char)
            input_string = input_string[1:]
            computation_trace.append((self.current_state.state_id, input_string))

        status = "ACCEPTED" if self.current_state.is_accepting else "REJECTED"
        return computation_trace, "{e}", status

    # ***************************************************************
    # reset
    # ***************************************************************
    # Purpose: Reset the DFA to its initial state.
    def reset(self):
        self.current_state = self.initial_state

# ***************************************************************
# main
# ***************************************************************
# Purpose: Entry point for the DFA simulator.
def main():
    try:
        dfa = DFALoader.load_from_file("./DFA.txt")
        print(">>>Loading DFA.txt…")
        while True:
            input_string = input(">>>Please enter a string to evaluate (or 'Quit' to exit): ")
            if input_string.lower() == 'quit':
                print(">>>Goodbye!")
                break
            computation_trace, ending_symbol, status = dfa.simulate(input_string)
            print(">>>Computation…")
            for i, (state, remaining_string) in enumerate(computation_trace[:-1]):
                next_string = computation_trace[i+1][1] if computation_trace[i+1][1] != "" else "{e}"
                if isinstance(computation_trace[i+1][0], str) and "INVALID INPUT" in computation_trace[i+1][0]:
                    print(f"{state},{remaining_string} -> INVALID INPUT")
                    break
                else:
                    print(f"{state},{remaining_string} -> {computation_trace[i+1][0]},{next_string}")
            print(status, end="\n\n")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
