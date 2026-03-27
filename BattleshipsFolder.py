import random as rand

playing = True

ship_initial = ["B|", "C|", "F|", "A|", "S|"]
ship_names = ["Battleship", "Cruiser", "Frigate", "Aircraft Carrier", "Submarine"]
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
    battleship_count = 0
    #Function for player placement ship
    while battleship_count <= number_of_ships-1:
        try:
            row = int(input(f"Enter the row for the {ship_names[battleship_count]}: "))-1
            col = int(input(f"Enter the column for the {ship_names[battleship_count]}: "))-1

            if viable_location(row, col):
                player_board[row][col] = ship_initial[battleship_count]
                occupied.add((row, col))
                battleship_count = battleship_count+1
            else:
                print("Invalid coordinates. Please enter correct value.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        #Increases the battleship value (from array) being printed.

    return player_board, occupied

def comp_ship_coordinate(comp_board):
    n = 0
    # Picks values between 0 and map_size * map_size and creates opponent board
    unique_array = rand.sample(range(0, map_size * map_size), len(ship_initial))
    for position in unique_array:
        x = position // map_size
        y = position % map_size
        comp_board[x][y] = f"{ship_initial[n]}"
        n = n + 1
    return comp_board

def get_input_from_player():
    #Collects player guess
    while True:
        try:
            row = int(input("\nEnter your row: "))-1
            col = int(input("Enter your col: "))-1
            if viable_location_hits(row, col):
                player_hit[row][col] = "Placeholder string. Will be replaced with either 'Hit' or 'Miss'."
                shots.add((row, col))
                break
            else:
                print("Invalid coordinates. Please enter correct values")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return row, col

def check_player_hit(comp_board, player_hit, row, col):
    #Player hit or missed on enemy ship
    if comp_board[row][col] == "B|":
        player_hit[row][col] = "H|"
        print("Computer Battleship has been hit!")
    elif comp_board[row][col] == "C|":
        player_hit[row][col] = "H|"
        print("Computer Cruiser has been hit!")
    elif comp_board[row][col] == "F|":
        player_hit[row][col] = "H|"
        print("Computer Frigate has been hit!")
    elif comp_board[row][col] == "A|":
        player_hit[row][col] = "H|"
        print("Computer Aircraft carrier has been hit!")
    elif comp_board[row][col] == "S|":
        player_hit[row][col] = "H|"
        print("Computer Submarine has been hit!")
    else:
        player_hit[row][col] = "M|"
        print("You missed!")
    return player_hit

def check_comp_hit(player_board, comp_hit, row, col):
    #Whether the computer hit or missed the player ship
    print(f"Computer guessed: Row {row+1}, Column {col+1}")
    if player_board[row][col] == "B|":
        comp_hit[row][col] = "H|"
        print("Player Battleship has been hit!")
    elif player_board[row][col] == "C|":
        comp_hit[row][col] = "H|"
        print("Player Cruiser has been hit!")
    elif player_board[row][col] == "F|":
        comp_hit[row][col] = "H|"
        print("Player Frigate has been hit!")
    elif player_board[row][col] == "A|":
        comp_hit[row][col] = "H|"
        print("Player Aircraft carrier has been hit!")
    elif player_board[row][col] == "S|":
        comp_hit[row][col] = "H|"
        print("Player Submarine has been hit!")

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
        return True
    elif comp_ships_hit == number_of_ships:
        print("\nGame over! The computer has sunk all your ships. You lose!")
        return True
    return False

while playing:
    print("\nBATTLESHIPS\n")
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
    guesses = (map_size**2)

    player_ship_coordinate(player_board, occupied)
    print("\nPlayer's board:")
    display_battlefield(player_board)

    while guesses > 0:
        #Player's turn
        print("\nIt's your turn to guess!")
        #Pluralization for guesses left
        if guesses > 1:
            print(f"You have {guesses} guesses left.")
        elif guesses == 1:
            print(f"You have {guesses} guess left.")
        row, col = get_input_from_player()
        check_player_hit(comp_board, player_hit, row, col)
        guesses = guesses-1
        print("\nYour guesses so far:")        
        display_battlefield(player_hit)

        #Computer's turn
        print("\nComputer's turn to guess!")
        position = comp_shots[guesses]
        row = position // map_size
        col = position % map_size
        check_comp_hit(player_board, comp_hit, row, col)
        display_battlefield(player_board)

        #Count number of ships hit
        player_ships_hit = sum(row.count("H|") for row in player_hit)
        comp_ships_hit = sum(row.count("H|") for row in comp_hit)

        #If guesses are 0, check who won and end game
        if guesses == 0:
            print("\nYou've used all your guesses.")
            if player_ships_hit == comp_ships_hit:
                print("\nGame over! You both sunk the same number of ships! It was a tie!")
                break
            elif player_ships_hit < comp_ships_hit:
                print("\nGame over! The computer has sunk more of your ships than you. You lose!")
                break
            elif player_ships_hit > comp_ships_hit:
                print("\nCongratulations! You've sunk more ships than the computer. You win!")

        #If all of board ships are gone, end turn loop
        allShipsGone = check_win(player_ships_hit, comp_ships_hit)
        if allShipsGone == True:
            guesses = 0

    #Point system.
    player_points = sum(row.count("H|") for row in player_hit) * 2 - sum(row.count("M|") for row in player_hit)
    comp_points = sum(row.count("H|") for row in comp_hit) * 2 - sum(row.count("M|") for row in player_hit)
    print(f"\nYour points: {player_points}")
    print(f"\nOpponent points: {comp_points}")
    playing = play_again()