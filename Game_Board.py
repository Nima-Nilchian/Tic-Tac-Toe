import pygame
import numpy as np

from constants import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(background_color)

class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0




class Game:
    def __init__(self):
        self.board = Board()
        self.show_lines()
        self.player = 1         # 1:Cross   #2:Circle


    def show_lines(self):
        # vertical
        pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
        pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

        # horizontal
        pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
        pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)


    def draw_fig(self, row, col):
        if self.player == 1:
            # Draw Cross
            # desc line
            start_desc = (col * square_size + offset, row * square_size + offset)
            end_desc = (col * square_size + square_size - offset, row * square_size + square_size - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)
            # asc line
            start_asc = (col * square_size + offset, row * square_size + square_size - offset)
            end_asc = (col * square_size + square_size - offset, row * square_size + offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)

        if self.player == 2:
            # Draw Circle
            center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
            pygame.draw.circle(screen, circ_color, center, radius, circ_width)



    def next_player(self):
        self.player = self.player % 2 + 1


