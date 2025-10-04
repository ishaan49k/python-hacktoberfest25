import random
import sys

SIZE = 5   # Grid size (5x5)
MINES = 5  # Number of mines

# Initialize grid and place mines
grid = [["." for _ in range(SIZE)] for _ in range(SIZE)]
mines = random.sample(range(SIZE * SIZE), MINES)

for m in mines:
    r, c = divmod(m, SIZE)
    grid[r][c] = "M"

# Count mines around a cell
def count_mines(r, c):
    if grid[r][c] == "M":
        return "M"
    count = 0
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            if 0 <= i < SIZE and 0 <= j < SIZE and grid[i][j] == "M":
                count += 1
    return str(count)

# Reveal cells recursively if zero mines nearby
def reveal_cells(r, c):
    if revealed[r][c] != ".":
        return  # Already revealed or flagged
    count = count_mines(r, c)
    revealed[r][c] = count
    if count == "0":
        # Reveal neighbors
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if 0 <= i < SIZE and 0 <= j < SIZE:
                    if revealed[i][j] == ".":
                        reveal_cells(i, j)

# Display grid with row and column numbers, show flags
def display_grid():
    print("\n    " + " ".join(str(i) for i in range(SIZE)))
    print("   " + "--" * SIZE)
    for idx, row in enumerate(revealed):
        display_row = []
        for cell, flag in zip(row, flags[idx]):
            if flag:
                display_row.append("🚩")
            else:
                display_row.append(cell)
        print(f"{idx} | " + " ".join(display_row))
    print()

# Initialize revealed and flags grid
revealed = [["." for _ in range(SIZE)] for _ in range(SIZE)]
flags = [[False for _ in range(SIZE)] for _ in range(SIZE)]

def check_win():
    safe_cells = SIZE * SIZE - MINES
    revealed_count = sum(cell != "." and cell != "🚩" for row in revealed for cell in row)
    return revealed_count == safe_cells

def input_move():
    while True:
        user_input = input("Enter row col (e.g. '1 3') or flag/unflag (e.g. 'f 2 4'): ").strip().lower()
        parts = user_input.split()
        
        if len(parts) == 2:
            # Reveal move
            try:
                r, c = int(parts[0]), int(parts[1])
                if 0 <= r < SIZE and 0 <= c < SIZE:
                    return ("reveal", r, c)
                else:
                    print("❌ Coordinates out of bounds, try again.")
            except:
                print("❌ Invalid input, use numbers for row and col.")
        elif len(parts) == 3 and parts[0] == 'f':
            # Flag/unflag move
            try:
                r, c = int(parts[1]), int(parts[2])
                if 0 <= r < SIZE and 0 <= c < SIZE:
                    return ("flag", r, c)
                else:
                    print("❌ Coordinates out of bounds, try again.")
            except:
                print("❌ Invalid input, use numbers for row and col after 'f'.")
        else:
            print("❌ Invalid input format. Try again.")

# Game loop
print("🎮 Welcome to Minesweeper! 🎮")
print("Reveal all safe cells without hitting a mine.")
print("To reveal, enter row and col separated by space (e.g., '1 2').")
print("To flag/unflag a cell, type 'f' followed by row and col (e.g., 'f 1 2').")

while True:
    display_grid()
    action, r, c = input_move()

    if action == "flag":
        if revealed[r][c] != ".":
            print("⚠️ Cannot flag a revealed cell.")
        else:
            flags[r][c] = not flags[r][c]
            print(f"{'🚩 Flagged' if flags[r][c] else '🚩 Unflagged'} cell ({r}, {c})")
        continue

    if flags[r][c]:
        print("⚠️ Cell is flagged. Unflag it first to reveal.")
        continue

    if grid[r][c] == "M":
        print("💥 BOOM! You hit a mine. Game Over.")
        # Reveal all mines
        for i in range(SIZE):
            for j in range(SIZE):
                if grid[i][j] == "M":
                    revealed[i][j] = "M"
        display_grid()
        sys.exit()

    reveal_cells(r, c)

    if check_win():
        display_grid()
        print("🏆 Congratulations! You cleared all safe cells!")
        break
