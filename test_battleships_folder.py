import os

# Clear the console
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create an empty board
def create_board(size=10):
    return [["~"] * size for _ in range(size)]

# Print the board (optionally hide ships)
def print_board(board, hide_ships=False):
    print("   " + " ".join(str(i) for i in range(len(board))))
    for idx, row in enumerate(board):
        if hide_ships:
            print(f"{idx:2} " + " ".join("~" if cell == "S" else cell for cell in row))
        else:
            print(f"{idx:2} " + " ".join(row))

# Ship definitions: name -> length
SHIP_TYPES = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}

# Check if ship can be placed
def can_place_ship(board, x, y, length, orientation):
    size = len(board)
    if orientation == "H":
        if y + length > size:
            return False
        return all(board[x][y+i] == "~" for i in range(length))
    elif orientation == "V":
        if x + length > size:
            return False
        return all(board[x+i][y] == "~" for i in range(length))
    return False

# Place ship on board
def place_ship(board, x, y, length, orientation):
    if orientation == "H":
        for i in range(length):
            board[x][y+i] = "S"
    elif orientation == "V":
        for i in range(length):
            board[x+i][y] = "S"

# Manual ship placement
def manual_place_ships(board):
    for ship, length in SHIP_TYPES.items():
        placed = False
        while not placed:
            print_board(board)
            print(f"Place your {ship} (length {length})")
            try:
                x = int(input("Enter starting row: "))
                y = int(input("Enter starting column: "))
                orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
                if orientation not in ["H", "V"]:
                    print("❌ Invalid orientation. Use H or V.")
                    continue
                if 0 <= x < len(board) and 0 <= y < len(board):
                    if can_place_ship(board, x, y, length, orientation):
                        place_ship(board, x, y, length, orientation)
                        placed = True
                    else:
                        print("❌ Cannot place ship there. Out of bounds or overlapping.")
                else:
                    print("❌ Coordinates out of range.")
            except ValueError:
                print("❌ Please enter valid integers.")

# Take a shot
def take_shot(board, tracking_board):
    size = len(board)
    while True:
        try:
            x = int(input("Enter row to fire at: "))
            y = int(input("Enter column to fire at: "))
            if 0 <= x < size and 0 <= y < size:
                if tracking_board[x][y] in ["H", "M"]:
                    print("❌ You already fired there!")
                else:
                    if board[x][y] == "S":
                        print("💥 Hit!")
                        tracking_board[x][y] = "H"
                        board[x][y] = "H"
                        return True
                    else:
                        print("💦 Miss!")
                        tracking_board[x][y] = "M"
                        return False
            else:
                print("❌ Coordinates out of range!")
        except ValueError:
            print("❌ Please enter valid integers.")

# Check if all ships are sunk
def all_ships_sunk(board):
    return all(cell != "S" for row in board for cell in row)

# Main game loop
def battleship_game():
    size = 10

    # Player boards
    p1_board = create_board(size)
    p2_board = create_board(size)

    # Tracking boards
    p1_tracking = create_board(size)
    p2_tracking = create_board(size)

    # Player 1 places ships
    print("=== Player 1: Place your ships ===")
    manual_place_ships(p1_board)
    input("Press Enter and pass to Player 2...")
    clear_screen()

    # Player 2 places ships
    print("=== Player 2: Place your ships ===")
    manual_place_ships(p2_board)
    input("Press Enter to start the battle...")
    clear_screen()

    # Game loop
    turn = 1
    while True:
        if turn == 1:
            print("=== Player 1's Turn ===")
            print("Your board:")
            print_board(p1_board)
            print("Opponent's board:")
            print_board(p1_tracking)
            take_shot(p2_board, p1_tracking)
            if all_ships_sunk(p2_board):
                print("🎉 Player 1 wins!")
                break
            turn = 2
        else:
            print("=== Player 2's Turn ===")
            print("Your board:")
            print_board(p2_board)
            print("Opponent's board:")
            print_board(p2_tracking)
            take_shot(p1_board, p2_tracking)
            if all_ships_sunk(p1_board):
                print("🎉 Player 2 wins!")
                break
            turn = 1
        input("Press Enter to switch turns...")
        clear_screen()

if __name__ == "__main__":
    battleship_game()