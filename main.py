class State:
    def __init__(self, state_id, is_accepting, transitions):
        self.state_id = state_id
        self.is_accepting = is_accepting
        self.transitions = transitions


class DFALoader:
    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            num_states = int(file.readline().strip())
            accepting_states = list(map(int, file.readline().split()))
            alphabet = file.readline().split()
            transitions = [list(map(int, file.readline().split())) for _ in range(num_states)]
            
        return DFA(num_states, accepting_states, alphabet, transitions)


class DFA:
    def __init__(self, num_states, accepting_states, alphabet, transitions):
        self.states = [State(i, i in accepting_states, transitions[i]) for i in range(num_states)]
        self.alphabet = alphabet
        self.initial_state = self.states[0]
        self.current_state = self.initial_state

    def transition(self, char):
        if char not in self.alphabet:
            raise ValueError(f"Invalid input character: {char}")
        next_state_idx = self.states.index(self.current_state)  # Get the index of the current state
        char_idx = self.alphabet.index(char)  # Get the index of the character in the alphabet
        self.current_state = self.states[self.current_state.transitions[char_idx]]  # Transition to the next state

    def simulate(self, input_string):
        self.reset()
        computation_trace = [(self.current_state.state_id, input_string)]

        for char in input_string:
            if char not in self.alphabet:
                computation_trace.append((self.current_state.state_id, f"INVALID INPUT: {char}"))
                return computation_trace, "", "REJECTED"
            self.transition(char)
            input_string = input_string[1:]  # Consume one character
            computation_trace.append((self.current_state.state_id, input_string))

        # Once the string is fully processed, check if the current state is accepting
        status = "ACCEPTED" if self.current_state.is_accepting else "REJECTED"
        return computation_trace, "{e}", status

    def reset(self):
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
                print(f"{state},{remaining_string} -> {computation_trace[i+1][0]},{next_string}")
            # Display the result
            print(status)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
