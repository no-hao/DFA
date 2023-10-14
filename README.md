# Deterministic Finite Automaton (DFA) Simulator

This project provides a simulator for Deterministic Finite Automatons (DFAs). DFAs are foundational in computer science, particularly in the theory of computation. This simulator allows users to define DFAs in a specific file format and then test strings against these DFAs to determine acceptance or rejection.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [DFA File Format](#dfa-file-format)
  - [Running the Simulator](#running-the-simulator)
- [Customization](#customization)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/no-hao/DFA.git
   ```

2. Navigate to the project directory:
   ```sh
   cd DFA
   ```

## Usage

### DFA File Format

The DFA is defined in a file (default: `DFA.txt`). The format is as follows:

1. The first line indicates the number of states.
2. The second line lists the accepting states.
3. The third line defines the alphabet.
4. Subsequent lines define state transitions.

Example:

```
3
2
a b c
1 2 0
2 2 3
1 3 2
```

### Running the Simulator

1. Execute the main script:
   ```sh
   python3 main.py
   ```

2. Follow the on-screen prompts to enter strings for evaluation. You can exit the simulator by typing `Quit`.

## Customization

- **Changing the DFA File**: 
  - If you want to use a different filename or path for your DFA definition, modify the following line in the `main()` function:
    ```python
    dfa = DFALoader.load_from_file("<Your-File-Path-Here>")
    ```

## License

This project is licensed under the MIT License.
