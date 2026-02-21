import random as rand
from random import randrange

playing = True

ship_initial = ["B|", "C|", "F|", "A|", "S|"]
ship_names = ["Battleship", "Cruiser", "Frigate", "Aircraft Carrier", "Sub"]
number_of_ships = len(ship_initial)

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
    # Picks 5 values between 0 and map_size * map_size and creates opponent board
    unique_array = rand.sample(range(0, map_size * map_size), len(ship_initial))
    for position in unique_array:
        x = position // map_size
        y = position % map_size
        comp_board[x][y] = "X|"
    return comp_board

def get_input_from_player():
    #Collects player guess
    while True:
        try:
            row = int(input("\nEnter your row: "))-1
            col = int(input("Enter your col: "))-1
            if viable_location_hits(row, col):
                player_hit[row][col] = "This does nothing.|"
                shots.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return row, col

def check_player_hit(comp_board, player_hit, row, col):
    #Player hit or missed on enemy ship
    if comp_board[row][col] == "X|":
        player_hit[row][col] = "H|"
        print("Computer Ship has been hit!")
    else:
        player_hit[row][col] = "M|"
        print("You missed!")
    return player_hit

def check_comp_hit(player_board, comp_hit, row, col):
    #Whether the computer hit or missed the player ship
    print(f"Computer guessed: Row {row+1}, Column {col+1}")
    if player_board[row][col] == "B|":
        comp_hit[row][col] = "B|"
        print("Player Battleship has been hit!")
    elif player_board[row][col] == "C|":
        comp_hit[row][col] = "C|"
        print("Player Cruiser has been hit!")
    elif player_board[row][col] == "F|":
        comp_hit[row][col] = "F|"
        print("Player Frigate has been hit!")
    elif player_board[row][col] == "A|":
        comp_hit[row][col] = "A|"
        print("Player Aircraft carrier has been hit!")
    elif player_board[row][col] == "S":
        comp_hit[row][col] = "S|"
        print("Player Sub has been hit!")

    else:
        comp_hit[row][col] = "M|"
        print("Opponent missed!")
    player_board[row][col] = "*|"
    return comp_hit

def play_again():
    while True:
        #Asks player if they want to play again and make lowercase for easier input
        play_again_input = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again_input in ["yes", "y"]:
            return True
        elif play_again_input in ["no", "n"]:
            print("Thanks for playing! Goodbye!")
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def check_win(player_ships_hit, comp_ships_hit):
    #Checks if player or computer has won the game
    if player_ships_hit == number_of_ships:
        print("\nCongratulations! You've sunk all the computer's ships. You win!")
        return False
    elif comp_ships_hit == number_of_ships:
        print("\nGame over! The computer has sunk all your ships. You lose!")
        return False
    return True

while playing:
    print("BATTLESHIPS\n")
    get_username()
    while True:
        try:
            map_size = int(input("\nChoose a map size between 5 and 50: "))
            if not (5 <= map_size <= 50):
                raise ValueError("Map size must be between 5 and 100.")
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter a valid integer.")

    player_board = create_battlefield(map_size)
    comp_board = create_battlefield(map_size)
    player_hit = create_battlefield(map_size)
    comp_hit = create_battlefield(map_size)
    comp_ship_coordinate(comp_board)
    comp_shots = rand.sample(range(0, map_size * map_size), (map_size * map_size))

    occupied = set()
    shots = set()
    opp = set()
    guesses = 10

    print("\nPlayer's board:")
    player_ship_coordinate(player_board, occupied)
    display_battlefield(player_board)

    for n in range(guesses):
        playing = check_win(player_hit, comp_hit)
        print("\nIt's your turn to guess!")
        row, col = get_input_from_player()
        check_player_hit(comp_board, player_hit, row, col)
        guesses=guesses-1
        print("\nYour guesses so far:")        
        display_battlefield(player_hit)
        if guesses > 1:
            print(f"You have {guesses} guesses left.")
        elif guesses == 1:
            print(f"You have {guesses} guess left.")

        print("\nComputer's turn to guess!")
        position = comp_shots[n]
        row = position // map_size
        col = position % map_size
        check_comp_hit(player_board, comp_hit, row, col)
        display_battlefield(player_board)

        #If guesses are 0, check who won and end game
        if guesses == 0:
            player_ships_hit = sum(row.count("H|") for row in player_hit)
            comp_ships_hit = sum(row.count("B|") + row.count("C|") + row.count("F|") + row.count("A|") + row.count("S|") for row in comp_hit)
            print("\nYou've used all your guesses.")
            if player_ships_hit > comp_ships_hit:
                print("\nCongratulations! You've sunk more computer ships than the computer. You win!")
                break
            elif player_ships_hit < comp_ships_hit:
                print("\nGame over! The computer has sunk more of your ships than you sunk. You lose!")
    playing = play_again()    
