# N-Puzzle Solver with GUI

This is a Python application that solves the N-Puzzle problem (8-Puzzle, 15-Puzzle, 24-Puzzle) using Best-First Search algorithm with multiple heuristics. It features a graphical user interface (GUI) built with Tkinter to visualize the puzzle and the solving process step-by-step.
this is project of AI in UNI 
---

## Features

- Supports 3 puzzle sizes:
  - 8-Puzzle (3x3)
  - 15-Puzzle (4x4)
  - 24-Puzzle (5x5)
- Multiple heuristics for the search algorithm:
  1. Misplaced Tiles
  2. Manhattan Distance
  3. Linear Conflict
  4. Euclidean Distance
- Shuffle puzzle tiles randomly.
- Interactive GUI to click and move tiles manually.
- Visual animation of the solution path after solving.
- Displays the number of moves in the solution.

---

## Installation

Make sure you have Python 3 installed.

No external dependencies are required besides the standard Python libraries.

---

## Usage

Run the main Python file:

```bash
python n_puzzle_solver.py
