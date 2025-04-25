import matplotlib.pyplot as plt

# board game
board = [
    [['A',0],['B',1],['B',4],['B',0],['C',1],['D',3],['D',0]],
    [['A',0],['A',0],['A',0],['B',2],['B',0],['D',0],['D',0]],
    [['A',0],['E',0],['E',0],['F',0],['F',0],['D',0],['G',0]],
    [['H',0],['E',0],['E',0],['F',0],['F',0],['G',4],['G',0]],
    [['H',0],['H',2],['H',0],['I',0],['J',0],['J',0],['G',0]],
    [['K',0],['H',0],['L',0],['L',0],['J',0],['J',0],['G',5]],
    [['K',0],['K',0],['L',0],['L',1],['J',3],['M',0],['M',0]]
]

row_len = len(board)
col_len = len(board[0])


unique_blocks = sorted(set(b[0] for row in board for b in row))

# ************** board grafic ***********************

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlim(0, col_len)
ax.set_ylim(0, row_len)

ax.invert_yaxis()  

# # Function to detect block boundaries
def draw_block_border(block_char):
    cells = [(r, c) for r in range(row_len) for c in range(col_len) if board[r][c][0] == block_char]
    
    for r, c in cells:
        num = board[r][c][1]
    # Check neighbors – if the neighbor is not in the same block, draw a thick line
        if r == 0 or board[r-1][c][0] != block_char:
            ax.plot([c, c+1], [r, r], color='black', linewidth=2)
        else:
            ax.plot([c, c+1], [r, r], color='black', linewidth=0.5)
        if r == row_len-1 or board[r+1][c][0] != block_char:
            ax.plot([c, c+1], [r+1, r+1], color='black', linewidth=2)
        else: 
            ax.plot([c, c+1], [r+1, r+1], color='black', linewidth=0.5)
        if c == 0 or board[r][c-1][0] != block_char:
            ax.plot([c, c], [r, r+1], color='black', linewidth=2)
        else:
            ax.plot([c, c], [r, r+1], color='black', linewidth=0.5)
        if c == col_len-1 or board[r][c+1][0] != block_char:
            ax.plot([c+1, c+1], [r, r+1], color='black', linewidth=2)
        else:
           ax.plot([c+1, c+1], [r, r+1], color='black', linewidth=0.5) 

           # add number value of the block
        ax.text(c + 0.5, r + 0.5, num, ha='center', va='center',
                fontsize=18, color='black', weight='bold')


#******************** solve algoritem ********************

def find_empty_block(blocks):
    for r in range(row_len):
        for c in range(col_len):  
            if blocks[r][c][1] == 0:

                return (r, c)
    return None

def find_block_size(block):
    block_size = 0
    for r in range(row_len):
        for c in range(col_len):  
            if board[r][c][0] == block:
                block_size += 1
    return block_size

def is_valid(board, num, pos):
       return is_valid_in_neighbors(board, num, pos) and is_valid_in_block(board, num, pos)

# checks if placing a specific number num in the given position pos is valid within the same block
def is_valid_in_block(board, num, pos):
    for r in range(row_len):
        for c in range(col_len):  
            
            if (pos[0] != r or pos[1] != c) and board[r][c][0] == board[pos[0]][pos[1]][0] and board[r][c][1] == num: 
                return False
    return True

# checks if position pos violates the rule of no repeated numbers in the neighboring 3×3 region surrounding the position.
def is_valid_in_neighbors(board, num, pos):
        r ,c = pos
     
        for i in range(r -1, r +2):
            for j in range(c-1, c+2):
                if i >= 0 and i < row_len and j >= 0 and j < col_len and ((i,j)  != pos):
                   if  board[i][j][1]== num:
                        return False
        
        return True

def solve():
    """
    Attempts to solve the irregular Sudoku puzzle using backtracking.
    - Finds the next empty cell.
    - Determines the size of the block that cell belongs to.
    - Tries all possible values from 1 to block_size.
    - Recursively continues if a valid number is placed.
    - Backtracks if needed.
    """

    find =  find_empty_block(board)
    if not find:
        return True
    else:
        row, col = find
        block_size = find_block_size(board[row][col][0])
        for num in range(1,block_size +1):
            if is_valid(board, num, find):
                board[row][col][1] = num

                if solve():
                    return True
                
                board[row][col][1] = 0

#for block in unique_blocks:
#    draw_block_border(block)
def main():
    solve()

    for block in unique_blocks:
        draw_block_border(block)

    print(find_block_size('L'))

    plt.title("Irregular Sudoku")
    plt.show()

if __name__ == "__main__":
    main()
