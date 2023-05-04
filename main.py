import pygame

WINDOW_SIZE = (300, 300)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("tic-tac-toe")
font = pygame.font.SysFont("Arial", 60)

def draw_board(board):
    # Loop through each row and column of the Tic Tac Toe board
    for i in range(3):
        for j in range(3):
            # Create a rectangular object for the current cell
            rect = pygame.Rect(j * 100, i * 100, 100, 100)
            # Draw the rectangular object on the screen with a white outline
            pygame.draw.rect(screen, WHITE, rect, 2)

            # If the current cell contains an "X", draw a white X in the cell
            if board[i * 3 + j] == "X":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.line(screen, WHITE, (x - 25, y - 25), (x + 25, y + 25), 2)
                pygame.draw.line(screen, WHITE, (x - 25, y + 25), (x + 25, y - 25), 2)
            # If the current cell contains an "O", draw a white circle in the cell
            if board[i * 3 + j] == "O":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.circle(screen, WHITE, (x, y), 25, 2)
    # Update the display to show the new board state
    pygame.display.update()


# This function is used to draw a message on the screen. It takes a text input as a parameter.
# It creates a font object and renders the text using the font. The font color is set to white.
# The rendered message is then blitted onto the screen at the center-top position.
def draw_message(text):
    font = pygame.font.Font(None, 36)  # create font object
    message = font.render(text, True, WHITE)  # render the text using the font and set the color to white
    screen.blit(message, (screen.get_width() // 2 - message.get_width() // 2, 50))  # blit the message onto the screen at the center-top position


# This function handles the player's action during the game. It takes the current game board and the player's symbol (X or 0) as parameters.
# It starts a loop that listens for mouse button down events.
# When the player clicks the mouse button, it retrieves the x and y coordinates of the mouse position.
# The x and y coordinates are used to determine the row and column of the clicked cell on the board.
# If the clicked cell is empty (contains a space character), the player's symbol is placed in that cell on the board.
# The active flag is then set to False to exit the loop and end the player's turn.
def player_action(board, player):
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # listen for mouse button down event
                x, y = pygame.mouse.get_pos()  # retrieve mouse coordinates
                i = y // 100  # calculate row index based on y coordinate
                j = x // 100  # calculate column index based on x coordinate
                if board[i * 3 + j] == " ":  # check if the clicked cell is empty
                    board[i * 3 + j] = player  # place the player's symbol in the clicked cell
                    active = False  # set active flag to False to exit the loop

# This function checks if the specified player has won the game. It takes the current game board and the player's symbol (X or 0) as parameters.
# It checks for all possible winning combinations on the board and returns True if any of them match the player's symbol.
# The function first checks for winning combinations in the rows by iterating over the rows of the board.
# If any row contains three consecutive cells with the player's symbol, it returns True.
# Then it checks for winning combinations in the columns by iterating over the columns of the board.
# If any column contains three consecutive cells with the player's symbol, it returns True.
# Finally, it checks for winning combinations in the diagonals.
# If either of the diagonals contains three consecutive cells with the player's symbol, it returns True.
# If none of the winning combinations match the player's symbol, it returns False indicating that the player has not won.
def check_win(board, player):
    for i in range(0, 9, 3):  # iterate over rows
        if board[i:i+3] == [player, player, player]:  # check for winning combination in rows
            return True
    for i in range(3):  # iterate over columns
        if board[i] == player and board[i+3] == player and board[i+6] == player:  # check for winning combination in columns
            return True
    if board[0] == player and board[4] == player and board[8] == player:  # check for winning combination in the main diagonal
        return True
    if board[2] == player and board[4] == player and board[6] == player:  # check for winning combination in the secondary diagonal
        return True
    return False  # no winning combination found, return False


import random
ai_player = "0"
human_player = "X"


def minimax(board, depth, is_maximizing):
    # If we've reached the maximum depth of the search, return 0
    if depth == 0:
        return 0

    # If we're trying to maximize our score
    if is_maximizing:
        # Start with a very low score
        best_score = -float('inf')
        # For each empty square on the board
        for i in range(len(board)):
            if board[i] == " ":
                # Make a move on the board and recursively call minimax for the other player
                board[i] = ai_player
                score = minimax(board, depth - 1, False)
                # Undo the move
                board[i] = " "
                # Update the best score we've seen so far
                best_score = max(score, best_score)
        # Return the best score we found
        return best_score
    else:
        # If we're trying to minimize our score, do the same as above but with the human player
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] == " ":
                board[i] = human_player
                score = minimax(board, depth - 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


# This function uses the minimax algorithm to determine the best move for the bot player.
# It tries all the available moves and calculates the score for each move using the minimax algorithm
# with the depth limit of 10. The higher the score, the better the move.
# If there are multiple moves with the same highest score, it randomly chooses one from them.
# Returns the index of the best move.

def get_bot_move(board):
    best_score = -float('inf')
    # Try all the available moves
    for i in range(len(board)):
        if board[i] == " ":
            board[i] = ai_player
            # Calculate the score for the move
            score = minimax(board, 10, False)
            board[i] = " "
            # Update the best score and move if necessary
            if score > best_score:
                best_score = score
                best_move = i
            # If the score is the same as the best score, choose randomly from the available moves
            else:
                available_move = [i for i in range(9) if board[i] == " "]
                best_move = random.choice(available_move)
    return best_move


def play_game():
    # Set up a new game board
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    # Draw the game board
    draw_board(board)

    # Set the players for the game, and randomly determine who goes first
    players = ["X", "0"]
    if random.choice([True, False]):
        players = players[::-1]

    # Set up the game loop
    game_over = False
    while not game_over:
        # Get the current player
        current_player = players[0]

        # If the current player is the computer, get the computer's move and make it
        if current_player == "0":
            bot_move = get_bot_move(board)
            board[bot_move] = current_player
            draw_board(board)

        # If the current player is a human, get their move and make it
        else:
            player_action(board, current_player)

        # Check if the current player has won the game
        if check_win(board, current_player):
            message = f"{current_player} win!!"
            game_over = True

        # Check if the game is a draw
        elif " " not in board:
            message = "Draw"
            game_over = True

        # Switch to the other player
        else:
            current_player = players[1]

            # If the current player is the computer, get the computer's move and make it
            if current_player == "0":
                bot_move = get_bot_move(board)
                board[bot_move] = current_player
                draw_board(board)

            # If the current player is a human, get their move and make it
            else:
                player_action(board, current_player)

            # Check if the current player has won the game
            if check_win(board, current_player):
                message = f"{current_player} win!!"
                game_over = True

            # Check if the game is a draw
            elif " " not in board:
                message = "Draw"
                game_over = True

        # Draw the updated game board
        draw_board(board)

    draw_message(message)
    pygame.display.update()
    pygame.time.delay(1000)

play_game()