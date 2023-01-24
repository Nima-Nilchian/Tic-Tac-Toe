import random
import sys

import pygame
import time
import numpy as np

from constants import *
from algorithm import AI

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(background_color)

class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0


    def winner(self, show=False):
        '''
            return 0 if there is no win yet
            return 1 if player X wins
            return 2 if player O wins
        '''

        # vertical wins
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circ_color if self.squares[0][col] == 2 else cross_color
                    i_pos = (col * square_size + square_size // 2, 20)
                    f_pos = (col * square_size + square_size // 2, height - 20)
                    pygame.draw.line(screen, color, i_pos, f_pos, line_width)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circ_color if self.squares[row][0] == 2 else cross_color
                    i_pos = (20, row * square_size + square_size // 2)
                    f_pos = (width - 20, row * square_size + square_size // 2)
                    pygame.draw.line(screen, color, i_pos, f_pos, line_width)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circ_color if self.squares[1][1] == 2 else cross_color
                i_pos = (20, 20)
                f_pos = (width - 20, height - 20)
                pygame.draw.line(screen, color, i_pos, f_pos, cross_width)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circ_color if self.squares[1][1] == 2 else cross_color
                i_pos = (20, height - 20)
                f_pos = (width - 20, 20)
                pygame.draw.line(screen, color, i_pos, f_pos, cross_width)
            return self.squares[1][1]

        # no win yet
        return 0

    # change the house of the board to the player number
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        # Randomize the list to prevent the algorithm play same thing every round
        random.shuffle(empty_sqrs)
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.home_page()
        self.player = -1        # 1: Cross   #2: Circle
        self.turn = 1
        self.gamemode = 'ai'    # aivsai or ai
        self.running = True


    def home_page(self):
        # Draw titles
        self.set_title('choose AI algorithm', 40)
        self.set_title('choose AI Difficulty', 180)
        self.set_title('Play Tic-Tac-Toe', 325)
        self.set_title('Reset game: (press r)', 465)
        self.set_title('change game mode: (press g)', 520)

        # Draw buttons
        minimax_button = pygame.Rect((width / 8), (height / 7), width / 4, 50)
        self.set_button(minimax_button, 'Minimax')
        alpha_beta_button = pygame.Rect(5 * (width / 8), (height / 7), width / 4, 50)
        self.set_button(alpha_beta_button, 'Alpha Beta')

        easy_button = pygame.Rect((width / 8), (height / 2.70), width / 4, 50)
        self.set_button(easy_button, 'Easy')
        hard_button = pygame.Rect(5 * (width / 8), (height / 2.70), width / 4, 50)
        self.set_button(hard_button, 'Hard')

        play_x_button = pygame.Rect((width / 8), (height / 1.65), width / 4, 50)
        self.set_button(play_x_button, 'Play as X')
        play_o_button = pygame.Rect(5 * (width / 8), (height / 1.65), width / 4, 50)
        self.set_button(play_o_button, 'Play as O')

        # handle events for the action
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if play_x_button.collidepoint(mouse):
                time.sleep(0.2)
                self.player = 1
                self.ai.ai_player = 2

            elif play_o_button.collidepoint(mouse):
                time.sleep(0.2)
                self.player = 2
                self.ai.ai_player = 1

            elif minimax_button.collidepoint(mouse):
                time.sleep(0.2)
                self.ai.algorithm = 1
                print('Minimax algorithm Chosen')

            elif alpha_beta_button.collidepoint(mouse):
                time.sleep(0.2)
                self.ai.algorithm = 2
                print('Alpha Beta algorithm Chosen')

            elif easy_button.collidepoint(mouse):
                time.sleep(0.2)
                self.ai.difficulty = 'easy'
                print('AI Plays Easy')

            elif hard_button.collidepoint(mouse):
                time.sleep(0.2)
                self.ai.difficulty = 'hard'
                print('AI Plays Hard')

            screen.fill(background_color)

    def set_button(self, play_x_button, text, ):
        play_x = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 20), text, True, black)
        play_x_rect = play_x.get_rect()
        play_x_rect.center = play_x_button.center
        pygame.draw.rect(screen, white, play_x_button)
        screen.blit(play_x, play_x_rect)

    def set_title(self, text, pos):
        title = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 28), text, True, white)
        title_rect = title.get_rect()
        title_rect.center = ((width / 2), pos)
        screen.blit(title, title_rect)

    def show_lines(self):
        # vertical
        pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
        pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

        # horizontal
        pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
        pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)

    def draw_fig(self, row, col):
        # Draw Cross
        if self.turn == 1:
            # desc line
            start_desc = (col * square_size + offset, row * square_size + offset)
            end_desc = (col * square_size + square_size - offset, row * square_size + square_size - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)
            # asc line
            start_asc = (col * square_size + offset, row * square_size + square_size - offset)
            end_asc = (col * square_size + square_size - offset, row * square_size + offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)

        # Draw Circle
        if self.turn == 2:
            center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
            pygame.draw.circle(screen, circ_color, center, radius, circ_width)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.turn)
        self.draw_fig(row, col)
        self.next_player()

    def next_player(self):
        self.turn = self.turn % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'aivsai' else 'aivsai'

    def isover(self):
        return self.board.winner(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()






