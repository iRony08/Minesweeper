import random

class Minesweeper:
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.mines = mines
        self.board = self.generate_board()
        self.revealed = set()
        self.flags = set()

    def generate_board(self):
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        mine_positions = random.sample(range(self.height * self.width), self.mines)

        for pos in mine_positions:
            row = pos // self.width
            col = pos % self.width
            board[row][col] = -1  # -1 represents a mine

            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.height and 0 <= j < self.width and board[i][j] != -1:
                        board[i][j] += 1
        return board

    def reveal(self, cell):
        row, col = cell
        if self.board[row][col] == -1:
            return False
        self._reveal_cell(row, col)
        return True

    def _reveal_cell(self, row, col):
        if (row, col) in self.revealed:
            return
        self.revealed.add((row, col))

        if self.board[row][col] == 0:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.height and 0 <= j < self.width:
                        self._reveal_cell(i, j)

    def is_mine(self, cell):
        row, col = cell
        return self.board[row][col] == -1

    def nearby_mines(self, cell):
        row, col = cell
        return self.board[row][col]

    def won(self):
        return len(self.revealed) == self.height * self.width - self.mines

class MinesweeperAI:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.revealed = set()

    def make_move(self):
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.revealed:
                    self.revealed.add((row, col))
                    return (row, col)
        return None
