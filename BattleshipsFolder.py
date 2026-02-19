from random import randrange

playing = True

print("BATTLESHIPS")
ship_initial = ["B|", "C|", "F|", "A|", "S|"]
ship_names = ["Battleship", "Cruiser", "Frigate", "Aircraft Carrier", "Sub"]


def get_username():
    """
    function getting username for welcome message
    """
    while True:
        user_name = input("\nEnter your name: ")
        if user_name:
            print(f"\nWelcome to the battleship game {user_name}!")
            return user_name
        else:
            print("Please enter your name.")

def get_map_size():
    try:
        map_size = int(input("\nChoose a map size between 5 and 100 (From 0): "))
    except ValueError or (100 < map_size < 5):
        print("\nInvalid input. Please enter a valid integer.")

def create_battlefield(map_size):

    return [["_|"] * (map_size-0) for _ in range(map_size-0)]


def display_battlefield(board):

    for row in board:
        print(" ".join(row))

def viable_location(row, col):
    return (0 <= row < map_size and 0 <= col < map_size and (row, col) not in occupied)

def viable_location_hits(row, col):
    return (0 <= row < map_size and 0 <= col < map_size and (row, col) not in shots)

def viable_location_comp(row, col):
    return (0 <= row < map_size and 0 <= col < map_size and (row, col) not in opp)

def player_ship_coordinate(player_board, occupied):
    """
    function for player placement ship
    """
    while True:
        try:
            row = int(input("Enter the row for Battleship: "))-1
            col = int(input("Enter the column for Battleship: "))-1

            if viable_location(row, col):
                player_board[row][col] = "B|"
                occupied.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct value.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            row = int(input("Enter the row for Cruiser: "))-1
            col = int(input("Enter the column for Cruiser: "))-1

            if viable_location(row, col):
                player_board[row][col] = "C|"
                occupied.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            row = int(input("Enter the row for Frigate: "))-1
            col = int(input("Enter the column for Frigate: "))-1

            if viable_location(row, col):
                player_board[row][col] = "F|"
                occupied.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            row = int(input("Enter the row for Aircraft Carrier: "))-1
            col = int(input("Enter the column for Aircraft Carrier: "))-1

            if viable_location(row, col):
                player_board[row][col] = "A|"
                occupied.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            row = int(input("Enter the row for Submarine: "))-1
            col = int(input("Enter the column for Submarine: "))-1

            if viable_location(row, col):
                player_board[row][col] = "S|"
                occupied.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    return player_board, occupied


def comp_ship_coordinate(comp_board):
    """
    function for computer opponent.
    """
    for ship in ship_initial:
        while True:
            row = randrange(0, map_size)
            col = randrange(0, map_size)
            if comp_board[row][col] == "|_|":
                # Check if the ship can be placed at the random location
                comp_board[row][col] = ship
                break
    return comp_board

def get_input_from_player():
    while True:
        row = int(input("\nEnter your row: "))-1
        col = int(input("Enter your col: "))-1
        try:
            if viable_location_hits(row, col):
                player_hit[row][col] = "*|"
                shots.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return row, col

def check_player_hit(comp_board, player_hit):
    """
    function for player hit or missed on enemy ship
    """
    row, col = get_input_from_player()
    
    if comp_board[row][col] == "B|":
        player_hit[row][col] = "B|"
        print("Computer: Battleship been hit!")
    elif comp_board[row][col] == "C|":
        player_hit[row][col] = "C|"
        print("Computer: Cruiser been hit!")
    elif comp_board[row][col] == "F|":
        player_hit[row][col] = "F|"
        print("Computer: Frigate been hit!")
    elif comp_board[row][col] == "A|":
        player_hit[row][col] = "A|"
        print("Computer: Aircraft Carrier been hit")
    elif comp_board[row][col] == "S|":
        player_hit[row][col] = "S|"
        print("Computer: Sub been hit")
    else:
        player_hit[row][col] = "M|"
        print("You missed!")
    

    return player_hit

def get_input_from_comp(): 
    while True:
        row = randrange(0, map_size)
        col = randrange(0, map_size)
        if viable_location_comp(row, col):
            comp_hit[row][col] = "*|"
            player_board[row][col] = "*|"
            opp.add((row, col))
            break
        else:
            did_it_work = False
    print(f"Computer guessed: Row {row+1}, Column {col+1}")
    return row, col

def check_comp_hit(player_board, comp_hit):
    """
    function for whether the computer hit or missed the player ship
    """
    row, col = get_input_from_comp()

    if player_board[row][col] == "B|":
        comp_hit[row][col] = "B|"
        print("Player: Battleship been hit!")
    elif player_board[row][col] == "C|":
        comp_hit[row][col] = "C|"
        print("Player: Cruiser been hit!")
    elif player_board[row][col] == "F|":
        comp_hit[row][col] = "F|"
        print("Player: Frigate been hit!")
    elif player_board[row][col] == "A|":
        comp_hit[row][col] = "A|"
        print("Player: Aircraft carrier been hit!")
    elif player_board[row][col] == "S|":
        comp_hit[row][col] = "S|"
        print("Player: Sub been hit!")
    else:
        comp_hit[row][col] = "M|"
        print("Opponent missed!")

    return comp_hit


while playing:

        get_username()
        while True:
            try:
                map_size = int(input("\nChoose a map size between 5 and 100: "))
                if not (5 <= map_size <= 100):
                    raise ValueError("Map size must be between 5 and 100.")
                else:
                    break
            except ValueError:
                print("\nInvalid input. Please enter a valid integer.")
        player_board = create_battlefield(map_size)
        comp_board = create_battlefield(map_size)
        player_hit = create_battlefield(map_size)
        comp_hit = create_battlefield(map_size)

        occupied = set()
        shots = set()
        guesses = 10

        print("\nPlayer's board:")
        player_ship_coordinate(player_board, occupied)
        display_battlefield(player_board)


    #Doesn't function: comp_ship_coordinate(comp_board)
        for n in range(10):
            print("\nIt's your turn to guess!")
            check_player_hit(comp_board, player_hit)
            guesses=guesses-1
            display_battlefield(player_board)
            print("\nYour guesses so far:")        
            display_battlefield(player_hit)
            print(f"You have {guesses} guesses left.")
            

            print("\nComputer's turn to guess!")
            check_comp_hit(player_board, comp_hit)
