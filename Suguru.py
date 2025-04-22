import tkinter as tk
from tkinter import messagebox

class SuguruGUI:
    def __init__(self, master):
        self.master = master
        master.title("Suguru Solver")

        self.size = 5
        self.entries = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.groups = [[0 for _ in range(self.size)] for _ in range(self.size)]

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                entry = tk.Entry(self.master, width=3, font=('Helvetica', 16), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

    def create_buttons(self):
        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=self.size, column=0, columnspan=self.size, pady=10)

        solve_btn = tk.Button(btn_frame, text="🔍 פתר", command=self.solve_gui, bg="#4CAF50", fg="white", font=('Helvetica', 12))
        solve_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(btn_frame, text="🧼 נקה", command=self.clear_board, bg="#f44336", fg="white", font=('Helvetica', 12))
        clear_btn.grid(row=0, column=1, padx=5)

    def get_board_and_groups(self):
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                val = self.entries[i][j].get()
                if val.isdigit():
                    row.append(int(val))
                else:
                    row.append(0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def clear_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)

    def solve_gui(self):
        board = self.get_board_and_groups()
        # קבוצות לדוגמה, תוכל להחליף או לבנות מחולל
        groups = [
            [1, 1, 2, 2, 2],
            [3, 1, 4, 5, 5],
            [3, 4, 4, 5, 6],
            [3, 7, 6, 6, 6],
            [7, 7, 8, 8, 8]
        ]
        if solve_suguru(board, groups):
            self.set_board(board)
        else:
            messagebox.showerror("שגיאה", "אין פתרון חוקי ללוח.")

# ===== אלגוריתם פתרון סוגורו (כמו מקודם) =====
def print_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else "." for cell in row))
    print()

def is_valid(board, groups, row, col, num):
    for i in range(-1, 2):
        for j in range(-1, 2):
            r, c = row + i, col + j
            if 0 <= r < len(board) and 0 <= c < len(board[0]):
                if (r, c) != (row, col) and board[r][c] == num:
                    return False
    group_id = groups[row][col]
    for r in range(len(board)):
        for c in range(len(board[0])):
            if groups[r][c] == group_id and board[r][c] == num:
                return False
    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None

def get_group_size(groups, group_id):
    return sum(cell == group_id for row in groups for cell in row)

def solve_suguru(board, groups):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    group_id = groups[row][col]
    max_num = get_group_size(groups, group_id)

    for num in range(1, max_num + 1):
        if is_valid(board, groups, row, col, num):
            board[row][col] = num
            if solve_suguru(board, groups):
                return True
            board[row][col] = 0
    return False

# הפעלת הממשק
if __name__ == "__main__":
    root = tk.Tk()
    app = SuguruGUI(root)
    root.mainloop()
