import tkinter as tk
import random

# グローバル変数
CELL_SIZE = 30
COLS = 10
ROWS = 20
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1], [1, 1]], # O
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]] # J
]
COLORS = ["cyan", "purple", "yellow", "green", "red", "orange", "blue"]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")
        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="black")
        self.canvas.pack()
        self.restart()

    def restart(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.speed = 500
        self.current_shape = self.new_shape()
        self.next_shape = self.new_shape()
        self.game_over = False
        self.root.bind("<KeyPress>", self.handle_keys)
        self.draw_board()
        self.root.after(self.speed, self.drop_shape)

    def new_shape(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {"shape": shape, "color": color, "x": COLS // 2 - len(shape[0]) // 2, "y": 0}

    def handle_keys(self, event):
        if self.game_over:
            return
        if event.keysym == "Left":
            self.move(-1, 0)
        elif event.keysym == "Right":
            self.move(1, 0)
        elif event.keysym == "Down":
            self.drop_shape()
        elif event.keysym == "Up":
            self.rotate_shape()
        elif event.keysym == "space":
            self.hard_drop()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.board[y][x])
        self.draw_shape(self.current_shape)

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * CELL_SIZE, y * CELL_SIZE, 
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, 
            fill=color, outline="black"
        )

    def draw_shape(self, shape_info):
        shape, color, x, y = shape_info["shape"], shape_info["color"], shape_info["x"], shape_info["y"]
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    self.draw_cell(x + dx, y + dy, color)

    def move(self, dx, dy):
        if not self.collision(self.current_shape, dx, dy):
            self.current_shape["x"] += dx
            self.current_shape["y"] += dy
            self.draw_board()

    def rotate_shape(self):
        shape = self.current_shape["shape"]
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        if not self.collision({"shape": rotated_shape, "color": self.current_shape["color"], "x": self.current_shape["x"], "y": self.current_shape["y"]}):
            self.current_shape["shape"] = rotated_shape
            self.draw_board()

    def collision(self, shape_info, dx=0, dy=0):
        shape, x, y = shape_info["shape"], shape_info["x"] + dx, shape_info["y"] + dy
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    if x + dx < 0 or x + dx >= COLS or y + dy >= ROWS or self.board[y + dy][x + dx]:
                        return True
        return False

    def drop_shape(self):
        if not self.collision(self.current_shape, 0, 1):
            self.current_shape["y"] += 1
        else:
            self.merge_shape()
            self.clear_lines()
            self.current_shape = self.next_shape
            self.next_shape = self.new_shape()
            if self.collision(self.current_shape):
                self.game_over = True
                self.canvas.create_text(COLS*CELL_SIZE//2, ROWS*CELL_SIZE//2, text="GAME OVER", fill="red", font=("Helvetica", 24))
                return
        self.draw_board()
        self.root.after(self.speed, self.drop_shape)

    def hard_drop(self):
        while not self.collision(self.current_shape, 0, 1):
            self.current_shape["y"] += 1
        self.drop_shape()

    def merge_shape(self):
        shape, color, x, y = self.current_shape["shape"], self.current_shape["color"], self.current_shape["x"], self.current_shape["y"]
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    self.board[y + dy][x + dx] = color

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = ROWS - len(new_board)
        self.board = [[0] * COLS for _ in range(lines_cleared)] + new_board
        self.score += lines_cleared
        if self.score // 10 > self.level:
            self.level += 1
            self.speed = max(100, self.speed - 50)

if __name__ == "__main__":
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()
