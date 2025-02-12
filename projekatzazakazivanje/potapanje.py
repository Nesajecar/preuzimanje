import random

# Konstantne veličine table
BOARD_SIZE = 5
NUM_SHIPS = 3

# Funkcija za generisanje prazne table
def create_board():
    return [["~"] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Funkcija za prikaz table
def print_board(board):
    for row in board:
        print(" ".join(row))

# Funkcija za postavljanje brodova na tablu
def place_ships(board):
    ships = []
    while len(ships) < NUM_SHIPS:
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        if board[row][col] != "B":
            board[row][col] = "B"
            ships.append((row, col))
    return ships

# Funkcija za proveru unosa korisnika
def valid_input():
    while True:
        try:
            row = int(input(f"Unesi red (0-{BOARD_SIZE-1}): "))
            col = int(input(f"Unesi kolonu (0-{BOARD_SIZE-1}): "))
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                return row, col
            else:
                print(f"Unos mora biti između 0 i {BOARD_SIZE-1}.")
        except ValueError:
            print("Unos mora biti broj.")

# Funkcija za potez
def make_move(board, ships):
    row, col = valid_input()
    if (row, col) in ships:
        print("Pogodak!")
        board[row][col] = "X"
        ships.remove((row, col))
        return True
    else:
        print("Promašaj!")
        board[row][col] = "O"
        return False

# Glavna funkcija igre
def play_game():
    board = create_board()
    ships = place_ships(board)
    turns = 5

    print("Dobrodošli u igru Potapanje brodova!")
    print_board(board)

    while turns > 0 and ships:
        print(f"\nPreostali potezi: {turns}")
        print_board(board)

        if make_move(board, ships):
            if not ships:
                print("Sve brodove ste potopili! Pobeda!")
                break
        else:
            turns -= 1

    if turns == 0:
        print("Izgubili ste! Brodovi su bili na ovim pozicijama:")
        for ship in ships:
            board[ship[0]][ship[1]] = "B"
        print_board(board)

# Pokretanje igre
if __name__ == "__main__":
    play_game()
