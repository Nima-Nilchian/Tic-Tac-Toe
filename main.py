import sys

from Game_Board import *

game = Game()
ai = game.ai
user = -1
alg = game.choose_ai()  # 1-minimax  2-alpha beta

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game.player == -1:
        game.home_page()
    else:
        game.show_lines()

        if game.player == game.turn and game.running:
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                pos = pygame.mouse.get_pos()
                row = pos[1] // square_size
                col = pos[0] // square_size

                if game.board.empty_sqr(row, col):
                    game.make_move(row, col)
        else:
            # AI initial call
            if game.gamemode == 'ai' and game.running:
                # update the screen
                pygame.display.update()

                row, col = ai.eval(game.board, alg)
                game.make_move(row, col)

        if game.isover():
            game.running = False
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = pygame.font.Font.render(pygame.font.SysFont('bahnschrift', 20), "Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    game.player = -1
                    game.reset()
                    ai = game.ai
                    alg = game.choose_ai()  # 1-minimax  2-alpha beta

    pygame.display.update()

