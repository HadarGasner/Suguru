import cv2
import pytesseract
import re
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

# ====================== TYPES ======================
# A cell is [hex_color, digit]; board is rows x cols of cells
Cell = List[object]
Board = List[List[Cell]]

# ====================== OCR & COLOR HELPERS ======================

def find_digits_in_cell(cell_rgb: np.ndarray) -> int:
    """
    Runs OCR (Tesseract) on a cropped RGB cell image and returns the first digit found.
    Returns 0 if no digit is detected.

    Notes:
    - Tesseract/OpenCV expect BGR for many operations; we convert accordingly.
    - For single-character cells, PSM 10/13 are often best; PSM 6 can work for short text.
    """
    if cell_rgb is None or cell_rgb.size == 0:
        return 0

    # Convert RGB -> BGR for OpenCV processing
    cell_bgr = cv2.cvtColor(cell_rgb, cv2.COLOR_RGB2BGR)

    # Grayscale
    gray = cv2.cvtColor(cell_bgr, cv2.COLOR_BGR2GRAY)

    # Adaptive threshold to highlight digits (white text on black background)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # Morphological ops to make strokes thicker and reduce noise
    kernel = np.ones((2, 2), np.uint8)
    proc = cv2.medianBlur(thresh, 3)
    proc = cv2.dilate(proc, kernel, iterations=1)

    # OCR: allow only digits; try PSMs that suit single symbols
    configs = [
        r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789',
        r'--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789',
        r'--oem 3 --psm 6  -c tessedit_char_whitelist=0123456789',
    ]

    text = ""
    for cfg in configs:
        t = pytesseract.image_to_string(proc, config=cfg)
        if t and re.search(r'\d', t):
            text = t
            break

    digits = re.findall(r'\d+', text)
    return int(digits[0]) if digits else 0


def find_cell_color_hex(cell_rgb: np.ndarray) -> str:
    """
    Returns an approximate background color in HEX (#RRGGBB).
    Samples a pixel ~20% into the cell to avoid borders.
    """
    h, w = cell_rgb.shape[:2]
    y = max(0, int(h * 0.2))
    x = max(0, int(w * 0.2))
    r, g, b = cell_rgb[y, x]
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"


# ====================== IMAGE -> BOARD ======================

def image_to_board(image_path: str, rows: int, cols: int) -> Board:
    """
    Splits the full puzzle image into a board of [hex_color, digit] cells.
    - Uses a dynamic inner margin to avoid grid lines.
    - Keeps cell crops in RGB for color + OCR pipeline.
    """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Could not read image at: {image_path}")

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    height, width = img_rgb.shape[:2]
    cell_h, cell_w = height // rows, width // cols

    board: Board = []
    for i in range(rows):
        row: List[Cell] = []
        for j in range(cols):
            # Dynamic inner margin (8% of min(cell_h, cell_w))
            margin = max(2, int(min(cell_h, cell_w) * 0.08))
            y1 = i * cell_h + margin
            y2 = (i + 1) * cell_h - margin
            x1 = j * cell_w + margin
            x2 = (j + 1) * cell_w - margin
            cell = img_rgb[y1:y2, x1:x2]

            digit = find_digits_in_cell(cell)
            color = find_cell_color_hex(cell)
            row.append([color, digit])
        board.append(row)
    return board


# ====================== SOLVER ======================

def find_empty_cell(board: Board) -> Optional[Tuple[int, int]]:
    """Returns the first (row, col) where digit == 0, or None if board is full."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c][1] == 0:
                return (r, c)
    return None


def block_size_for_color(board: Board, color_hex: str) -> int:
    """Counts how many cells share the same block color."""
    return sum(1 for row in board for col in row if col[0] == color_hex)


def is_valid_in_block(board: Board, num: int, pos: Tuple[int, int]) -> bool:
    """Number must not appear twice within the same colored block."""
    r0, c0 = pos
    color = board[r0][c0][0]
    for r in range(len(board)):
        for c in range(len(board[0])):
            if (r, c) != (r0, c0) and board[r][c][0] == color and board[r][c][1] == num:
                return False
    return True


def is_valid_in_neighbors(board: Board, num: int, pos: Tuple[int, int]) -> bool:
    """
    Number must not appear in any of the 8 neighboring cells
    (Moore neighborhood).
    """
    r0, c0 = pos
    R, C = len(board), len(board[0])
    for r in range(r0 - 1, r0 + 2):
        for c in range(c0 - 1, c0 + 2):
            if 0 <= r < R and 0 <= c < C and (r, c) != (r0, c0):
                if board[r][c][1] == num:
                    return False
    return True


def is_valid(board: Board, num: int, pos: Tuple[int, int]) -> bool:
    """Combined constraints: block + neighborhood."""
    return is_valid_in_block(board, num, pos) and is_valid_in_neighbors(board, num, pos)


def solve(board: Board) -> bool:
    """
    Backtracking solver:
    - Valid numbers for a cell are 1..(size of its colored block).
    - Uses neighbor and block constraints.
    """
    empty = find_empty_cell(board)
    if not empty:
        return True
    r, c = empty

    bsize = block_size_for_color(board, board[r][c][0])
    for num in range(1, bsize + 1):
        if is_valid(board, num, (r, c)):
            board[r][c][1] = num
            if solve(board):
                return True
            board[r][c][1] = 0
    return False


# ====================== DRAWING ======================

def draw_board(ax, board: Board, title: str = "Irregular Sudoku Solver") -> None:
    """
    Draws the whole board:
    - Thick borders around block edges
    - Digits centered
    """
    R, C = len(board), len(board[0])

    # Helpful axis settings
    ax.set_xlim(0, C)
    ax.set_ylim(0, R)
    ax.set_xticks(range(C + 1))
    ax.set_yticks(range(R + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.invert_yaxis()  # row 0 at top

    # Draw per block cell borders + digits
    unique_blocks = sorted(set(cell[0] for row in board for cell in row))
    for block_color in unique_blocks:
        for r in range(R):
            for c in range(C):
                if board[r][c][0] != block_color:
                    continue

                num = board[r][c][1]
                # Edges: thicker if it's a block boundary or puzzle boundary
                lw_default = 0.6
                lw_thick = 2.0

                # Top edge
                top_is_boundary = r == 0 or board[r - 1][c][0] != block_color
                ax.plot([c, c + 1], [r, r], color='black',
                        linewidth=lw_thick if top_is_boundary else lw_default)

                # Bottom edge
                bottom_is_boundary = r == R - 1 or board[r + 1][c][0] != block_color
                ax.plot([c, c + 1], [r + 1, r + 1], color='black',
                        linewidth=lw_thick if bottom_is_boundary else lw_default)

                # Left edge
                left_is_boundary = c == 0 or board[r][c - 1][0] != block_color
                ax.plot([c, c], [r, r + 1], color='black',
                        linewidth=lw_thick if left_is_boundary else lw_default)

                # Right edge
                right_is_boundary = c == C - 1 or board[r][c + 1][0] != block_color
                ax.plot([c + 1, c + 1], [r, r + 1], color='black',
                        linewidth=lw_thick if right_is_boundary else lw_default)

                # Digit at center
                ax.text(c + 0.5, r + 0.5, str(num),
                        ha='center', va='center',
                        fontsize=18, color='black', weight='bold')

    ax.set_title(title)


# ====================== MAIN ======================

if __name__ == "__main__":
    # Path to the *unsolved* puzzle image
    image_path = input("please enter board image path")

    # Build initial board from image (6 rows x 5 cols)
    board = image_to_board(image_path, rows=6, cols=5)

    # Solve in-place
    _ = solve(board)

    # Draw result
    fig, ax = plt.subplots(figsize=(6, 6))
    draw_board(ax, board)
    plt.show()
