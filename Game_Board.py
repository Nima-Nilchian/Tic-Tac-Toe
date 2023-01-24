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
                    iPos = (col * square_size + square_size // 2, 20)
                    fPos = (col * square_size + square_size // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circ_color if self.squares[row][0] == 2 else cross_color
                    iPos = (20, row * square_size + square_size // 2)
                    fPos = (width - 20, row * square_size + square_size // 2)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circ_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circ_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # no win yet
        return 0


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
        self.player = -1        # 1:Cross   #2:Circle
        self.turn = 1
        self.gamemode = 'ai'    # pvp or ai
        self.running = True


    def home_page(self):
        # self.ai.algorithm = self.choose_ai()      # 1-minimax  2-alpha beta

        # Draw title
        title = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 28), "Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 150)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 20), "Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 20), "Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                self.player = 1
                self.ai.player = 2
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                self.player = 2
                self.ai.player = 1


            screen.fill(background_color)

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

    def choose_ai(self):
        sys.stdout.write(
            "Choose AI. [1/2]\n1. Minimax\n2. Alpha-Beta Pruning\n")
        answer = input().lower()
        if answer == "1":
            return 1
        elif answer == "2":
            return 2
        else:
            sys.stdout.write("Please respond with '1', '2'.\n")

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.winner(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

    # def which_turn(self):





