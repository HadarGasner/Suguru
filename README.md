# --- File: README.md ---

# 🧩 Irregular Sudoku Solver (with Visualization)

This project is a Python implementation of an **irregular Sudoku solver** (also known as a "Jigsaw Sudoku") with graphical board visualization using **matplotlib**.
you can find the game here: https://www.ynet.co.il/games
---

## 🎯 What It Does

- Solves an irregular Sudoku puzzle using **recursive backtracking**
- Enforces two rules:
  1. No repeated numbers in the same block
  2. No repeated numbers in the 3×3 neighboring area around any cell
- Visualizes the Sudoku board with:
  - Thick borders between irregular blocks
  - Number values shown in the center of each cell

---

## 📋 File Structure

```
irregular_sudoku.py     # Main script with board setup, logic, and visualization
```

---

## 🧠 How It Works

- `board` – a 7×7 grid where each cell is `[block_name, value]`
- `solve()` – recursive backtracking solver
- `is_valid()` – checks if a number is valid by block and neighborhood rules
- `draw_block_border()` – visualizes block edges and numbers using matplotlib

---

## 🖼️ Example Output

Running the code will display a colored grid of the Sudoku puzzle, with each irregular block outlined and filled with the solved numbers.

---

## ▶️ How to Run

```bash
python irregular_sudoku.py
```

Make sure you have `matplotlib` installed:
```bash
pip install matplotlib
```

---

## 🔧 Dependencies

- Python 3.x
- `matplotlib`

---

## 📝 Notes

- The irregular blocks are defined manually in the `board` variable.
- The solver uses recursive backtracking without heuristics.

---
