import sys

import pygame

from Game_Board import *

game = Game()
ai = game.ai
user = -1
alg = 1
# alg = game.choose_ai()  # 1-minimax  2-alpha beta

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # g-gamemode
            if event.key == pygame.K_g:
                game.change_gamemode()
                print(f'game mode changed to {game.gamemode}')

            # r-restart
            if event.key == pygame.K_r:
                game.reset()
                board = game.board
                ai = game.ai
                screen.fill(background_color)
                print('game restarted')

    if game.player == -1:
        game.home_page()
        alg = ai.algorithm
    else:
        game.show_lines()

        if game.player == game.turn and game.running and game.gamemode == 'ai':
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                pos = pygame.mouse.get_pos()
                row = pos[1] // square_size
                col = pos[0] // square_size

                if game.board.empty_sqr(row, col):
                    game.make_move(row, col)
        else:
            # AI Turn
            if game.running:
                # update the screen
                pygame.display.update()

                row, col = ai.eval(game.board, game.turn, game.gamemode, alg)
                game.make_move(row, col)
                time.sleep(0.5)

        if game.isover():
            game.running = False
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            game.set_button(againButton, 'Play Again')

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    game.player = -1
                    game.reset()
                    game.gamemode = 'ai'
                    ai = game.ai

    pygame.display.update()

