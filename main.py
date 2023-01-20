import sys

from Game_Board import *

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            row = pos[1] // square_size
            col = pos[0] // square_size

            if game.board.empty_sqr(row, col):
                game.board.mark_sqr(row, col, game.player)
                game.draw_fig(row, col)
                game.next_player()


    pygame.display.update()

