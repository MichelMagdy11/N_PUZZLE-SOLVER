import tkinter as tk
from tkinter import messagebox
import heapq
from math import sqrt
from random import shuffle
from itertools import count
class PuzzleState:
    def __init__(self, board, empty_pos, moves=0, parent=None):
        self.board = board
        self.empty_pos = empty_pos
        self.moves = moves
        self.parent = parent
        self.size = len(board)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))

    def is_goal(self, goal):
        return self.board == goal

    def get_path(self):
        path = []
        state = self
        while state:
            path.append(state.board)
            state = state.parent
        return path[::-1]


def get_successors(state):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    successors = []
    x, y = state.empty_pos
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < state.size and 0 <= ny < state.size:
            new_board = [row[:] for row in state.board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            successors.append(PuzzleState(new_board, (nx, ny), state.moves + 1, state))
    return successors


def misplaced_tiles(state, goal_positions):
    return sum(1 for i in range(state.size) for j in range(state.size)
               if state.board[i][j] != 0 and (i, j) != goal_positions[state.board[i][j]])


def manhattan_distance(state, goal_positions):
    distance = 0
    for i in range(state.size):
        for j in range(state.size):
            tile = state.board[i][j]
            if tile != 0:
                goal_x, goal_y = goal_positions[tile]
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance


def linear_conflict(state, goal_positions):
    conflict = 0
    for i in range(state.size):
        for j in range(state.size):
            tile = state.board[i][j]
            if tile != 0:
                goal_x, goal_y = goal_positions[tile]
                if i == goal_x:
                    for k in range(j + 1, state.size):
                        other_tile = state.board[i][k]
                        if other_tile != 0 and goal_positions[other_tile][0] == i and goal_positions[other_tile][1] < goal_y:
                            conflict += 1
                if j == goal_y:
                    for k in range(i + 1, state.size):
                        other_tile = state.board[k][j]
                        if other_tile != 0 and goal_positions[other_tile][1] == j and goal_positions[other_tile][0] < goal_x:
                            conflict += 1
    return manhattan_distance(state, goal_positions) + 2 * conflict


def euclidean_distance(state, goal_positions):
    distance = 0
    for i in range(state.size):
        for j in range(state.size):
            tile = state.board[i][j]
            if tile != 0:
                goal_x, goal_y = goal_positions[tile]
                distance += sqrt((i - goal_x) ** 2 + (j - goal_y) ** 2)
    return distance


def best_first_search(initial_state, goal_state, heuristic):
    open_set = []
    goal_positions = {goal_state[i][j]: (i, j) for i in range(len(goal_state)) for j in range(len(goal_state))}
    counter = count()
    heapq.heappush(open_set, (heuristic(initial_state, goal_positions), next(counter), initial_state))
    closed_set = set()

    while open_set:
        _, __, current_state = heapq.heappop(open_set)
        if current_state.is_goal(goal_state):
            return current_state.get_path()
        closed_set.add(current_state)
        for successor in get_successors(current_state):
            if successor not in closed_set:
                heapq.heappush(open_set, (heuristic(successor, goal_positions), next(counter), successor))
    return None


class NPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Puzzle Solver")
        self.size = 3
        self.board = []
        self.tiles = []
        self.empty_pos = (self.size - 1, self.size - 1)
        self.goal = []
        self.create_widgets()

    def create_widgets(self):
        self.size_frame = tk.Frame(self.root)
        self.size_frame.pack(pady=10)
        size_label = tk.Label(self.size_frame, text="Choose Puzzle Size:")
        size_label.pack(side=tk.LEFT)

        self.size_var = tk.IntVar(value=3)

        tk.Radiobutton(self.size_frame, text="8-Puzzle (3x3)", variable=self.size_var, value=3, command=self.reset_board).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(self.size_frame, text="15-Puzzle (4x4)", variable=self.size_var, value=4, command=self.reset_board).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(self.size_frame, text="24-Puzzle (5x5)", variable=self.size_var, value=5, command=self.reset_board).pack(side=tk.LEFT, padx=5)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.shuffle_board)
        self.shuffle_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        self.solve_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.heuristic_var = tk.IntVar(value=1)
        heuristic_label = tk.Label(self.root, text="Select Heuristic: 1) Misplaced  2) Manhattan  3) Linear Conflict  4) Euclidean")
        heuristic_label.pack(pady=10)
        self.heuristic_menu = tk.OptionMenu(self.root, self.heuristic_var, 1, 2, 3, 4)
        self.heuristic_menu.pack(pady=10)

        self.reset_board()

    def reset_board(self):
        self.size = self.size_var.get()
        self.goal = [[(i * self.size + j + 1) % (self.size * self.size) for j in range(self.size)] for i in range(self.size)]
        self.board = [[(i * self.size + j + 1) % (self.size * self.size) for j in range(self.size)] for i in range(self.size)]
        self.empty_pos = (self.size - 1, self.size - 1)

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(self.frame, text="", width=4, height=2, font=("Helvetica", 20), command=lambda x=i, y=j: self.tile_clicked(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.update_board()

    def shuffle_board(self):
        tiles = [tile for row in self.board for tile in row]
        shuffle(tiles)
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = tiles.pop(0)
                if self.board[i][j] == 0:
                    self.empty_pos = (i, j)

        self.update_board()

    def update_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.buttons[i][j].config(text="", state=tk.DISABLED)
                else:
                    self.buttons[i][j].config(text=str(self.board[i][j]), state=tk.NORMAL)

    def tile_clicked(self, x, y):
        ex, ey = self.empty_pos
        if (abs(x - ex) == 1 and y == ey) or (abs(y - ey) == 1 and x == ex):
            self.board[ex][ey], self.board[x][y] = self.board[x][y], self.board[ex][ey]
            self.empty_pos = (x, y)
            self.update_board()

    def solve_puzzle(self):
        initial_state = PuzzleState(self.board, self.empty_pos)
        heuristics = [misplaced_tiles, manhattan_distance, linear_conflict, euclidean_distance]
        heuristic = heuristics[self.heuristic_var.get() - 1]
        path = best_first_search(initial_state, self.goal, heuristic)
        if path:

            messagebox.showinfo("Solved", f"Puzzle solved in {len(path) - 1} moves!")

            for board in path:
                self.board = board
                self.empty_pos = next((i, j) for i in range(self.size) for j in range(self.size) if board[i][j] == 0)
                self.update_board()
                self.root.update()
                self.root.after(200)  # delay to visualize steps
        else:
            messagebox.showerror("No solution found!", "No solution was found for the given puzzle.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NPuzzleGUI(root)
    root.mainloop()
