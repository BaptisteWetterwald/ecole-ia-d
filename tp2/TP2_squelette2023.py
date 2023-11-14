import tkinter as tk
from tkinter import ttk
import numpy as np
import random as rnd
from threading import Thread
from queue import Queue
import time

symbol_type = [" ", "X", "O"]

player_type = ['human', 'AI: Min-Max', 'AI: alpha-beta']

def alpha_beta_decision(board, turn, queue):
    start = time.time()
    player = game.current_player()
    moves = board.get_possible_moves()
    best_move = moves[0]
    best_value = -2
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        value = min_value_alpha_beta(new_board, turn + 1, player%2 + 1, -2, 2)
        if value > best_value:
            best_move = move
            best_value = value
    queue.put(best_move)
    end = time.time()
    print("Time elapsed (alpha-beta): " + str(end - start))


def minimax_decision(board, turn, queue):
    start = time.time()
    player = game.current_player()
    moves = board.get_possible_moves()
    best_move = moves[0]
    best_value = -2
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        value = min_value(new_board, turn + 1, player%2 + 1)
        if value > best_value:
            best_move = move
            best_value = value
    queue.put(best_move)
    end = time.time()
    print("Time elapsed (min-max): " + str(end - start))


def max_value(board, turn, player):
    if board.check_victory():
        return -1
    if turn > 9:
        return 0
    value = -2
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        min_val = min_value(new_board, turn + 1, player%2 + 1)
        value = max(value, min_val)
    return value

def min_value(board, turn, player):
    if board.check_victory():
        return 1
    if turn > 9:
        return 0
    value = 2
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        max_val = max_value(new_board, turn + 1, player%2 + 1)
        value = min(value, max_val)
    return value


def min_value_alpha_beta(board, turn, player, alpha, beta):
    if board.check_victory():
        return 1
    if turn > 9:
        return 0
    value = 2
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        value = min(value, max_value_alpha_beta(new_board, turn + 1, player%2 + 1, alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

def max_value_alpha_beta(board, turn, player, alpha, beta):
    if board.check_victory():
        return -1
    if turn > 9:
        return 0
    value = -2
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_symbol(move, player, False)
        value = max(value, min_value_alpha_beta(new_board, turn + 1, player%2 + 1, alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value
    
class Board:
    
    grid = np.zeros((3, 3))
    drawn_symbols = list() # permet d'avoir une référence sur les caractères textuels du canvas créés

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reinit(self):
        self.grid.fill(0)
        for drawn_symbol in self.drawn_symbols:
            canvas1.delete(drawn_symbol)

    def get_possible_moves(self):
        possible_moves = list()
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    possible_moves.append((i, j))
        return possible_moves

    def add_symbol(self, position, player, update_display=True):
        self.grid[position[0]][position[1]] = player
        if update_display:
            self.drawn_symbols.append(canvas1.create_text((position[0] + 0.5) * (width // 3), (position[1] + 0.5) * (height // 3),
                            font=("helvetica", width // 6), text=symbol_type[player],
                            fill='purple'))
    
    def position_filled(self, position):
        return self.grid[position[0]][position[1]] != 0

    def check_victory(self):
        # Horizontal alignment check
        for i in range(3):
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != 0:
                return True
        # Vertical alignment check
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != 0:
                return True
        # Diagonal alignment check
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != 0:
            return True
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != 0:
            return True
        return False


class TicTacToe:

    def __init__(self):
        self.board = Board()
        self.human_turn = False
        self.turn = 1
        self.players = (0, 0) # deux joueurs humains
        self.ai_move = Queue()

    def current_player(self):
        return 2 - (self.turn % 2)

    def launch(self):
        self.board.reinit()
        self.turn = 0
        information['fg'] = 'black'
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, position):
        if not self.board.position_filled(position): # si non : possibilité de superposer des symboles
            self.board.add_symbol(position, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            position = (event.x // (width // 3), event.y // (height // 3))
            self.move(position)

    def ai_turn(self, ai_type):
        if ai_type == 1:  # Min-Max
            t = Thread(target=minimax_decision, args=(self.board, self.turn, self.ai_move)) # les mouvements sont stockés dans ai_move
            t.start()
            self.ai_wait_for_move()
        elif ai_type == 2:  # Alpha-Beta
            t = Thread(target=alpha_beta_decision, args=(self.board, self.turn, self.ai_move)) # idem
            t.start()
            self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if not self.ai_move.empty():
            self.move(self.ai_move.get())
        else:
            window.after(100, self.ai_wait_for_move)

    def handle_turn(self):
        self.human_turn = False
        if self.board.check_victory():
            information['fg'] = 'red'
            information['text'] = "Player " + str(self.current_player()) + " wins !"
            return
        elif self.turn >= 9:
            information['fg'] = 'red'
            information['text'] = "This a draw !"
            return
        self.turn = self.turn + 1
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        if self.players[self.current_player() - 1] != 0:
            self.human_turn = False
            self.ai_turn(self.players[self.current_player() - 1])
        else:
            self.human_turn = True


game = TicTacToe()

# Graphical settings
width = 300
height = 300
grid_thickness = 5

window = tk.Tk()
window.title("MApMS")
canvas1 = tk.Canvas(window, bg="pink", width=width, height=height)

# Grid drawing
line1 = canvas1.create_line(0, height // 3, width, height // 3, fill='white', width=grid_thickness)
line2 = canvas1.create_line(0, (height // 3) * 2, width, (height // 3) * 2, fill='white', width=grid_thickness)
line3 = canvas1.create_line(width // 3, 0, width // 3, height, fill='white', width=grid_thickness)
line4 = canvas1.create_line((width // 3) * 2, 0, (width // 3) * 2, height, fill='white', width=grid_thickness)

canvas1.grid(row=0, column=0, columnspan=2)

information = tk.Label(window, text="")
information.grid(row=1, column=0, columnspan=2)

label_player1 = tk.Label(window, text="Player 1: ")
label_player1.grid(row=2, column=0)
combobox_player1 = ttk.Combobox(window, state='readonly')
combobox_player1.grid(row=2, column=1)

label_player2 = tk.Label(window, text="Player 2: ")
label_player2.grid(row=3, column=0)
combobox_player2 = ttk.Combobox(window, state='readonly')
combobox_player2.grid(row=3, column=1)

combobox_player1['values'] = player_type
combobox_player1.current(0)
combobox_player2['values'] = player_type
combobox_player2.current(1)

button2 = tk.Button(window, text='New game', command=game.launch)
button2.grid(row=5, column=0)

button = tk.Button(window, text='Quit', command=window.destroy)
button.grid(row=5, column=1)

# Mouse handling
canvas1.bind('<Button-1>', game.click)

window.mainloop()
