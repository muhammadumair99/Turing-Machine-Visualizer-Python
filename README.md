# Turing Machine Visualizer Python

A modern graphical Turing Machine simulator built with Python and CustomTkinter. This application allows users to visualize Turing Machine execution in real time, test formal language recognizers, and create custom machines through a JSON-based ruleset editor.

## Overview

Turing Machine Visualizer Python is designed as an educational and development tool for students, educators, and computer science enthusiasts studying:

* Theory of Computation
* Automata Theory
* Formal Languages
* Context-Free Languages
* Context-Sensitive Languages
* Turing Machine Design

The simulator provides an intuitive interface for observing tape operations, state transitions, and machine execution step by step.

## Features

### Real-Time Tape Visualization

* Interactive tape display
* Head position highlighting
* Dynamic tape updates during execution

### Execution Controls

* Load and test input strings
* Single-step execution
* Automatic execution mode
* Adjustable simulation speed
* Reset machine state instantly

### Built-In Language Presets

Includes predefined Turing Machines for:

* aⁿbⁿ (Context-Free Language)
* aⁿbⁿcⁿ (Context-Sensitive Language)
* aⁿb²ⁿ Language
* Binary Palindrome Recognition

### Custom JSON Rulesets

* Create your own Turing Machines
* Edit transitions directly in the built-in editor
* Apply custom configurations without restarting the application
* JSON validation and error handling

### Diagnostics Panel

* Current state monitoring
* Rule execution logs
* Accept and reject state indicators
* Undefined transition detection

## Screenshots

Add screenshots of:

* Main interface
* Tape visualization
* JSON rules editor
* Execution logs
* Accepted and rejected machine states

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/turing-machine-visualizer-python.git
cd turing-machine-visualizer-python
```

### Install Dependencies

```bash
pip install customtkinter
```

### Run the Application

```bash
python main.py
```

## Example Ruleset Format

```json
{
  "start_state": "q0",
  "accept_state": "q_accept",
  "reject_state": "q_reject",
  "alphabet": ["a", "b"],
  "transitions": {
    "q0,a": ["q1", "X", "R"],
    "q1,b": ["q_accept", "b", "R"]
  }
}
```

### Transition Syntax

```text
current_state,current_symbol
       ↓
[next_state, write_symbol, direction]
```

Example:

```json
"q0,a": ["q1", "X", "R"]
```

Meaning:

* Read symbol `a` in state `q0`
* Write `X`
* Move Right
* Transition to state `q1`

## Technologies Used

* Python 3
* CustomTkinter
* Tkinter Canvas
* JSON

## Educational Applications

This project can be used for:

* Automata Theory coursework
* Theory of Computation labs
* Demonstrating Turing Machine algorithms
* Learning formal language recognition
* Academic projects and presentations

## Future Enhancements

* Multi-tape Turing Machine support
* State diagram visualization
* Save and load machine configurations
* Transition table editor
* Machine execution history
* Export simulation results

## Author

Created as an educational tool for visualizing and experimenting with Turing Machines and Formal Languages by Muhammad Umair
