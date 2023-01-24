import copy
import math
import random


class AI:

    def __init__(self, player=2):
        self.player = player
        self.algorithm = 1          # 1- minimax    2-alpha beta

    # --- MINIMAX ---
    def minimax(self, board, maximizing):
        # terminal case
        case = board.winner()

        # player X wins
        if case == 1:
            return 1, None  # eval, move
        # player O wins
        if case == 2:
            return -1, None
        # draw
        if board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval_ = self.minimax(temp_board, False)[0]
                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval_ = self.minimax(temp_board, True)[0]
                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = (row, col)

            return min_eval, best_move

    # MAIN EVAL
    def eval(self, main_board, alg=1):

        maximizer = False
        if self.player == 1:
            maximizer = True

        a, b = -math.inf, math.inf
        if alg == 1:
            eval_, move = self.minimax(main_board, maximizer)
        else:
            eval_, move = self.alpha_beta(main_board, maximizer, a, b)

        # print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval_}')

        return move  # row, col


    def alpha_beta(self, board, maximizing, a, b):
        # terminal case
        case = board.winner()

        # player X wins
        if case == 1:
            return 1, None  # eval, move
        # player O wins
        if case == 2:
            return -1, None
        # draw
        if board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval_ = self.alpha_beta(temp_board, False, a, b)[0]
                if eval_ > max_eval:
                    max_eval = eval_
                    best_move = (row, col)
                if max_eval >= b:
                    print('Beta cut')
                    break

                a = max(a, max_eval)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval_ = self.alpha_beta(temp_board, True, a, b)[0]
                if eval_ < min_eval:
                    min_eval = eval_
                    best_move = (row, col)
                if min_eval <= a:
                    print('alpha cut')
                    break

                b = min(b, min_eval)

            return min_eval, best_move


