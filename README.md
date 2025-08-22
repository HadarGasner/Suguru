# 🧩 Irregular Sudoku Solver (with Visualization)

This project is a Python implementation of an **irregular Sudoku solver** (also known as a "Jigsaw Sudoku")from an image.
It uses OpenCV and Tesseract OCR to read the puzzle, extract digits and block colors, and then applies a backtracking solver with the puzzle’s specific constraints.
The solved board is displayed using Matplotlib..
you can find the game here: https://www.ynet.co.il/games
---

## 🎯 What It Does

- Extract board from an image and display as array
- Solves an irregular Sudoku puzzle using **recursive backtracking**
- Visualizes the Sudoku board with

---

## Features
- 🖼️ Load puzzle directly from an image (PNG/JPG).
- 🔎 OCR (Optical Character Recognition) with Tesseract to detect given digits.
- 🎨 Block detection via color sampling.
- 🧮 Backtracking solver with
- 📊 Visualization of the solved board with clear block boundaries.
- 📑 Numeric solution as a table for validation.

---

## 📋 File Structure

```
irregular_sudoku.py     # Main script with board setup, logic, and visualization
```

---

## 🧠 How Solve Works

- `board` – a 6x5 grid where each cell is `[block_color, value]`
- `solve()` – recursive backtracking solver
- `is_valid()` –  checks if placing a number num at position (row, col) is allowed
    Block rule: Ensures num does not already exist in the same irregular block (cells with the same color).
    Neighborhood rule: Ensures num does not exist in the 3×3 neighborhood around the cell.
    Returns True if the number can be placed safely, otherwise False.
- `draw_block_border()` – visualizes block edges and numbers using matplotlib

---

## 🖼️ Example Input
The solver expects a **puzzle image** as input.  
The image should contain:
- A rectangular puzzle grid (default: 6 rows × 5 columns).
- Colored regions that define the irregular blocks.
- Digits (if given) placed inside some of the cells.  

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

## Requirements
Make sure you have the following installed:

- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)  
  (on Windows: install and add path to `tesseract.exe`)
- Python packages:
  ```bash
  pip install opencv-python pytesseract numpy matplotlib pandas

---

## 📝 Notes

- The irregular blocks are defined manually in the `board` variable.
- The solver uses recursive backtracking without heuristics.
- For best OCR results, use clear, high-contrast images.

---
