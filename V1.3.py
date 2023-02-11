import random
import string
import tkinter as tk

class WordSearchGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Generator")
        self.root.geometry("400x400")

        self.words = []
        self.grid = []
        self.rows = 0
        self.cols = 0

        self.words_label = tk.Label(self.root, text="Words (comma separated)")
        self.words_label.pack()
        self.words_entry = tk.Entry(self.root)
        self.words_entry.pack()
        self.rows_label = tk.Label(self.root, text="Rows")
        self.rows_label.pack()
        self.rows_entry = tk.Entry(self.root)
        self.rows_entry.pack()
        self.cols_label = tk.Label(self.root, text="Columns")
        self.cols_label.pack()
        self.cols_entry = tk.Entry(self.root)
        self.cols_entry.pack()

        self.generate_button = tk.Button(self.root, text="Generate", command=self.generate)
        self.generate_button.pack()

        self.result = tk.StringVar()
        self.result_label = tk.Label(self.root, textvariable=self.result)
        self.result_label.pack()

    def generate(self):
        self.words = self.words_entry.get().split(',')
        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())

        self.grid = [[random.choice(string.ascii_lowercase) for j in range(self.cols)] for i in range(self.rows)]

        for word in self.words:
            placed = False
            while not placed:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                direction = random.choice(['horizontal', 'vertical', 'diagonal'])

                if direction == 'horizontal':
                    if col + len(word) <= self.cols:
                        can_place = True
                        for k, letter in enumerate(word):
                            if self.grid[row][col + k] != '*' and self.grid[row][col + k] != letter:
                                can_place = False
                                break
                        if can_place:
                            for k, letter in enumerate(word):
                                self.grid[row][col + k] = letter
                            placed = True
                elif direction == 'vertical':
                    if row + len(word) <= self.rows:
                        can_place = True
                        for k, letter in enumerate(word):
                            if self.grid[row + k][col] != '*' and self.grid[row + k][col] != letter:
