class State:
    """
    Represents a state in a Deterministic Finite Automaton (DFA).
    """
    def __init__(self, state_id, is_accepting, transitions):
        """
        Initialize a new State.

        :param state_id: The unique identifier for this state.
        :param is_accepting: Boolean indicating if this state is an accepting state.
        :param transitions: List of transitions for each input symbol.
        """
        self.state_id = state_id
        self.is_accepting = is_accepting
        self.transitions = transitions


class DFALoader:
    """
    Utility class to load a DFA from a file.
    """
    @staticmethod
    def load_from_file(filename):
        """
        Load a DFA from a given file.

        :param filename: Path to the file.
        :return: An instance of DFA.
        """
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
    def __init__(self, num_states, accepting_states, alphabet, transitions):
        """
        Initialize a new DFA.

        :param num_states: Total number of states.
        :param accepting_states: List of accepting states.
        :param alphabet: List of input symbols.
        :param transitions: Matrix representing state transitions.
        """
        self.states = [State(i, i in accepting_states, transitions[i]) for i in range(num_states)]
        self.alphabet = alphabet
        self.initial_state = self.states[0]
        self.current_state = self.initial_state

    def transition(self, char):
        """
        Transition to the next state based on the given input character.

        :param char: Input character.
        """
        if char not in self.alphabet:
            raise ValueError(f"Invalid input character: {char}")
        next_state_idx = self.states.index(self.current_state)
        char_idx = self.alphabet.index(char)
        self.current_state = self.states[self.current_state.transitions[char_idx]]

    def simulate(self, input_string):
        """
        Simulate the DFA for a given input string.

        :param input_string: String to be evaluated.
        :return: Tuple containing the computation trace, ending symbol, and status.
        """
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

    def reset(self):
        """
        Reset the DFA to its initial state.
        """
        self.current_state = self.initial_state


def main():
    # Load DFA from the local file
    try:
        dfa = DFALoader.load_from_file("./DFA.txt")  # Use the local DFA.txt
        print(">>>Loading DFA.txt…")
        while True:
            # Get input string from the user
            input_string = input(">>>Please enter a string to evaluate (or 'Quit' to exit): ")
            if input_string.lower() == 'quit':
                print(">>>Goodbye!")
                break
            computation_trace, ending_symbol, status = dfa.simulate(input_string)
            print(">>>Computation…")
            # Display the computation with line breaks
            for i, (state, remaining_string) in enumerate(computation_trace[:-1]):
                next_string = computation_trace[i+1][1] if computation_trace[i+1][1] != "" else "{e}"
                # Check if the next state is "INVALID INPUT"
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
