import pygame

WINDOW_SIZE = (300, 300)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("tic-tac-toe")
font = pygame.font.SysFont("Arial", 60)

def draw_board(board):
    for i in range(3):
        for j in range(3):

            rect = pygame.Rect(j * 100, i * 100, 100, 100)
            pygame.draw.rect(screen, WHITE, rect, 2)

            if board[i * 3 + j] == "X":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.line(screen, WHITE, (x - 25, y - 25), (x + 25, y + 25), 2)
                pygame.draw.line(screen, WHITE, (x - 25, y + 25), (x + 25, y - 25), 2)
            if board[i * 3 + j] == "0":
                x = j * 100 + 50
                y = i * 100 + 50
                pygame.draw.circle(screen, WHITE, (x, y), 25, 2)
    pygame.display.update()

def draw_message(text):
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, WHITE)
    screen.blit(message, (screen.get_width() // 2 - message.get_width() // 2, 50))

def player_action(board, player):
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = y // 100
                j = x // 100
                if board[i * 3 + j] == " ":
                    board[i * 3 + j] = player
                    active = False
def check_win(board, player):
    for i in range(0, 9, 3):
        if board[i:i+3] == [player, player, player]:
            return True
    for i in range(3):
        if board[i] == player and board[i+3] == player and board[i+6] == player:
            return True
    if board[0] == player and board[4] == player and board[8] == player:
        return True
    if board[2] == player and board[4] == player and board[6] == player:
        return True
    return False

import random
ai_player = "0"
human_player = "X"
def minimax(board, depth, is_maximizing):
    if depth == 0:
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(len(board)):
            if board[i] == " ":
                board[i] = ai_player
                score = minimax(board, depth - 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] == " ":
                board[i] = human_player
                score = minimax(board, depth - 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def get_bot_move(board):
    best_score = -float('inf')
    for i in range(len(board)):
        if board[i] == " ":
            board[i] = ai_player
            score = minimax(board, 10, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
            else:
                available_move = [i for i in range(9) if board[i] == " "]
                best_move = random.choice(available_move)
    return best_move

def play_game():
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    draw_board(board)
    game_over = False
    players = ["X", "0"]
    if random.choice([True, False]):
        players = players[::-1]
    while not game_over:
        current_player = players[0]
        if current_player == "0":
            bot_move = get_bot_move(board)
            board[bot_move] = current_player
            draw_board(board)
        else:
            player_action(board, current_player)
        if check_win(board, current_player):
            message = f"{current_player} win!!"
            game_over = True
        elif " " not in board:
            message = "Draw"
            game_over = True
        else:
            current_player = players[1]
            if current_player == "0":
                bot_move = get_bot_move(board)
                board[bot_move] = current_player
                draw_board(board)
            else:
                player_action(board, current_player)
            if check_win(board, current_player):
                message = f"{current_player} win!!"
                game_over = True
            elif " " not in board:
                message = "Draw"
                game_over = True
        draw_board(board)

    draw_message(message)
    pygame.display.update()
    pygame.time.delay(1000)

play_game()