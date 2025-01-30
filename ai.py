from board import Board
from constants import PLAYER1_PIECE_COLOR, PLAYER2_PIECE_COLOR, ROWS, COLS
from game import Game
import board_configs
import random
import unittest


# TO DO: Implement this function. The four lines currently implemented including the return are in place to make the
# gameplay visualization work. Replace all of it with your own code for the function.


def minimax_alpha_beta(board, depth, alpha, beta, max_player, game, eval_params=None):
    """
        Executes the Minimax algorithm with Alpha-Beta pruning to determine the optimal move in a two-player game.

        Args:
            board (Board): The current board state
            depth (int): The maximum depth to go to on the search tree
            alpha (float): The best value that the maximizing player can guarantee
            beta (float): The best value that the minimizing player can guarantee
            max_player (bool): True if the current player is the maximizing player (AI), False if minimizing (human)
            game (Game): The game instance
            eval_params (tuple, optional): A tuple of weights for evaluating the board state.

        Returns:
            tuple: A tuple (evaluation, best_move) where:
                - score (float): The score for the best move at this depth
                - best_move (Board): The board state after the best move
        """



    player = PLAYER2_PIECE_COLOR if max_player else PLAYER1_PIECE_COLOR

    moves = game.generate_all_moves(board, player)
    if depth == 0:
        return (evaluate(board, game, *eval_params) if eval_params else evaluate(board,game)), board
    
    best_move, best_score = None, float('-inf') if max_player else float('inf')
    
  
    

    #comparator = max if max_player else min

    #print(f"COUNTMOVES::{len(moves)}::DEPTH::{depth}")
    for move in moves:
        #print(f"DEPTH::{depth}::INDEX::{index}")


        scr, _ = minimax_alpha_beta(move, depth-1, alpha, beta, not max_player, game, eval_params)
        #proj_score = evaluate(move, game, eval_params)
        
        #print(f"MINIMAX::/ SCORE: {scr}::{max_player}:::{depth}:: ")

        #brd.print_board_config(brd.to_board_config())
        #best_move, best_score = comparator((best_score, best_move), (scr, brd))
        if max_player:
            if scr > best_score:
                best_move, best_score = move, scr

            #best_move.print_board_config(best_move.to_board_config())
            alpha = max(best_score, alpha)
            if beta <= alpha:
                break
        
        elif not max_player:

            if scr < best_score:
                best_move, best_score = move, scr

            beta = min(best_score, beta)
            if alpha >= beta:
                break
    
    if best_move is None:
        #return board
    #     print('none')
         best_move = board
         best_score = float('-inf') if max_player else float('inf')

    #     return (evaluate(board, game, *eval_params) if eval_params else evaluate(board,game)), best_move

    return best_score, best_move

def find_moves(board, piece):

    possible = []
    
    incr_moves = [(piece.row + 1, piece.col + 1), (piece.row + 1, piece.col - 1)]

    decr_moves = [(piece.row - 1, piece.col + 1), (piece.row - 1, piece.col - 1)]


    king_moves = incr_moves + decr_moves

    if piece.king:
        moves = king_moves
    else:
        moves = incr_moves if piece.color == PLAYER2_PIECE_COLOR else decr_moves

    opp_color = PLAYER2_PIECE_COLOR if piece.color == PLAYER1_PIECE_COLOR else PLAYER1_PIECE_COLOR
    #print(f"FIND MOVES///:king:{piece.king}:", end = ' ')
    #print(moves)
    for move in moves:

        if not move[0] < ROWS or not move[1] < COLS or not move[0] >= 0 or not move[1] >= 0:
            #print(f"FIND MOVES///:OUT OF BOUNDS::: PIECE AT point({piece.row}, {piece.col}) couln't move to {move[0]}, {move[1]}  ")
            continue



        spot = board.get_piece(move[0], move[1])
        #print(f"FIND MOVES///:SPOT VALUE:::  ", end = ' ')
        #print(f"SPOT:: {str(spot)}, OPP COLOR:: {str(opp_color)}, PIECE COLOR: {piece.color}")
        #print(spot == 0)
        #print(f"spot type {type(spot)} vs opp type: {type(opp_color)}")
        #if hasattr(spot, 'color'):
            #print("same type:")
            #print(spot.color == opp_color)


        if spot == 0:
            #print(f"FIND MOVES///:NOT OCCUPPIED::: PIECE AT point({piece.row}, {piece.col}) can move to {move[0]}, {move[1]}  ")


            possible.append(move)
            continue
        elif spot.color == opp_color:
            #print(f"FIND MOVES///:OPP COLOR::: PIECE AT point({piece.row}, {piece.col}) couldn't move to {move[0]}, {move[1]}  ")

            row_incr =  1 if piece.row < move[0] else -1
            col_incr =  1 if piece.col < move[1] else -1

            new_mv = (move[0] + row_incr, move[1] + col_incr)

            #print(f"FIND MOVES///:OPP COLOR::: try to go to {new_mv[0]}, {new_mv[1]}  ")

            if not new_mv[0] < ROWS or not new_mv[1] < COLS or not new_mv[0] >= 0 or not new_mv[1] >= 0:
                continue
            #might return out of bounds
            if board.get_piece(new_mv[0], new_mv[1]) == 0:
                #print(f"FIND MOVES///:CAPTURE::: PIECE AT point({piece.row}, {piece.col}) can to {move[0]}, {move[1]}")

                possible.append(new_mv)
        #print('=' * 100)

    return possible

def evaluate(board, game, pieces_weight=1.0, kings_weight=1.0, moves_weight=0.0, opportunities_weight=0.0, king_hopefuls_weight=0.0):
    """
    Evaluates the given board and returns a score based on a weighted combination of these metrics:

        1. The difference in the number of own pieces vs. opponent pieces
        2. The difference in the number of own kings vs. opponent kings
        3. The difference in the number of own king hopefuls vs. opponent king hopefuls (See Notes below)
        4. The difference in the number of capture opportunities for the player vs. the opponent
        5. The difference in the number of moves available for the player vs. the opponent.

    The AI player (using Minimax) is assumed to be Player 2.

    Args:
        board (Board): The current state of the game board
        game (Game): The game instance
        pieces_weight (float): Weight for the difference in piece count
        kings_weight (float): Weight for the difference in king count
        moves_weight (float): Weight for the difference in available moves
        opportunities_weight (float): Weight for the difference in capture opportunities
        king_hopefuls_weight (float): Weight for the difference in king hopefuls.

    Returns:
        float: A score representing the board's goodness for Player 2

    Notes:
        - King hopefuls have to do with pieces that can become king in the next move and are counted not just as the
        number of such pieces but as how many such king promotions can occur. So, if a piece can become king in its
        next move in two ways, then the piece is counted twice.
    """

    p1_num_pieces, p1_num_kings, p1_num_moves, p1_num_opportunities, p1_num_king_hopefuls = counts(board, game, PLAYER1_PIECE_COLOR)
    p2_num_pieces, p2_num_kings, p2_num_moves, p2_num_opportunities, p2_num_king_hopefuls = counts(board, game, PLAYER2_PIECE_COLOR)

    # print('EVAL: ' + '='*100)
    # print(f'p1: {p1_num_pieces}')
    # print(f'p2: {p2_num_pieces}')
 

    pieces_diff = p2_num_pieces - p1_num_pieces
    kings_diff = p2_num_kings - p1_num_kings
    moves_diff = p2_num_moves - p1_num_moves
    opportunities_diff = p2_num_opportunities - p1_num_opportunities
    king_hopefuls_diff = p2_num_king_hopefuls - p1_num_king_hopefuls
    #print(pieces_weight)
    score = (pieces_diff * pieces_weight +
             kings_diff * kings_weight +
             moves_diff * moves_weight +
             opportunities_diff * opportunities_weight +
             king_hopefuls_diff * king_hopefuls_weight)

    return score

# TO DO: Implement this function.
def counts(board, game, color):
    """
    Counts various metrics for pieces of a given color on the board.

    Args:
        board (Board): The current board state
        game (Game): The game instance
        color (tuple): The RGB color of the pieces to evaluate, formatted as a tuple (e.g., (255, 240, 125)).

    Returns:
        A tuple containing:
        - num_pieces (int): The number of pieces of the specified color on the board
        - num_kings (int): The number of kings of the specified color
        - num_moves (int): The total number of available single-hop moves for all pieces of the specified color
        - num_opportunities (int): The total number of capture opportunities across all pieces of the specified color
        - num_king_hopefuls (int): The total number of moves that lead to king promotions for the specified color.
    """

    num_pieces = num_kings = num_moves = num_opportunitites = num_king_hopefuls = 0
    for i in range(ROWS):
        for j in range(COLS):
            #print(f"COUNTS//: CHECKING POINT::: {i}, {j}")
            piece = board.get_piece(i, j)
            #print('COUNTS//: PIECE:::', end=' ')
            #print(piece)
            # if hasattr(piece, 'color'):
            #     print('COUNTS//: PIECE COLOR:::', end = ' ')
            #     print(piece.color)
            #     print(f"COLOR// COMPARING THE COLORS: {str(piece.color)} vs {str(color)}")
            #     print(piece.color == color)

            if piece != 0 and piece.color == color:
                #print("DID ENTER")
                num_pieces += 1
                if piece.king:
                    num_kings += 1

                moves = find_moves(board, piece)
                num_moves += len(moves)
                for move in moves:

                    #print(f"COUNTS//:for move in moves::: PIECE AT point({piece.row}, {piece.col}) to ({move[0]}, {move[1]})")
                    if abs(move[0] - i) == 2:
                        #print(f"JUMP::: PIECE AT point({piece.row}, {piece.col}) captured a piece and is at {move[0]}, {move[1]}  ")

                        num_opportunitites += 1
                    #else:
                        #print(f"NOTHING::: PIECE AT point({piece.row}, {piece.col}) to {move[0]}, {move[1]}  isn't a capture")

                    if not piece.king and game.check_king_hopeful(piece,  move[0], piece.row, piece.col ):
                        num_king_hopefuls += 1
                
    #print('',num_pieces, num_kings, num_moves, num_opportunitites, num_king_hopefuls )
    return num_pieces, num_kings, num_moves, num_opportunitites, num_king_hopefuls 

def compare_boards(board1, board2):
    """
    Compares two board objects to determine if they are identical in piece layout, piece color, and piece status (king or non-king).

    Args:
        board1 (Board): The first board object to compare.
        board2 (Board): The second board object to compare.

    Returns:
        bool: True if the boards are identical in terms of piece layout, piece color, and king status at each position; False otherwise

    The function checks each position (row, col) on an 8x8 board grid:
    - If both positions are empty (denoted by 0), it continues to the next position.
    - If only one position is empty, it returns False.
    - If both positions contain a piece, it checks that the pieces have the same color and king status. If any discrepancy is found, it returns False.

    Assumptions:
        - `board1` and `board2` are expected to have a `get_piece(row, col)` method that  returns either a piece object
        (with `color` and `king` attributes) or 0 if the position is empty.
    """

    if not isinstance(board1, Board) or not isinstance(board2, Board):
        return False

    for row in range(8):
        for col in range(8):
            piece1 = board1.get_piece(row, col)
            piece2 = board2.get_piece(row, col)

            if piece1 == 0 and piece2 == 0:
                continue

            if (piece1 == 0) != (piece2 == 0):
                return False

            if piece1.color != piece2.color or piece1.king != piece2.king:
                return False

    return True


class AiTest(unittest.TestCase):

    def test_counts_with_boards(self):
        for b in range(0, 6):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            game = Game()
            colors = [PLAYER1_PIECE_COLOR, PLAYER2_PIECE_COLOR]

            piece_counts = [[7, 13], [7, 12], [6, 12], [1, 11], [1, 10], [2, 12]]
            king_counts  = [[2, 2], [2, 3], [3, 2], [1, 0], [1, 0], [1, 0]]
            move_counts  = [[8, 17], [10, 14], [7, 11], [0, 12], [1, 12], [0, 12]]
            opportunity_counts  = [[3, 4], [4, 3], [1, 3], [0, 0], [1, 0], [0, 1]]
            king_hopeful_counts  = [[0, 0], [1, 0], [1, 0], [0, 2], [0, 2], [0, 2]]
            print("CONFIG:" + '='*30)
            board.print_board_config(board.to_board_config())

            for c in range(2):

                color = colors[c]
                num_pieces, num_kings, num_moves, num_opportunities, num_king_hopefuls = counts(board, game, color)
                self.assertEqual(num_pieces, piece_counts[b][c])
                self.assertEqual(num_kings, king_counts[b][c])
                self.assertEqual(num_moves, move_counts[b][c])
                self.assertEqual(num_opportunities, opportunity_counts[b][c])
                self.assertEqual(num_king_hopefuls, king_hopeful_counts[b][c])

    def test_evaluate_1(self):

        expected_scores = [6.0, 6.0, 5.0, 9.0, 8.0, 9.0, 8.0, 10.0, 10.0, 4.0, 3.0, 4.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_2(self):

        expected_scores = [16.0, 8.0, 10.0, 23.0, 20.0, 24.0, 22.0, 25.0, 23.0, 9.0, 10.0, 13.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, moves_weight=1.0, opportunities_weight=1.0, king_hopefuls_weight=1.0)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_3(self):

        expected_scores = [11.0, 7.25, 7.75, 15.5, 13.5, 16.0, 14.5, 16.75, 16.0, 6.25, 6.25, 8.25]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, pieces_weight=1.0, kings_weight=1.0, moves_weight=0.5, opportunities_weight=0.5, king_hopefuls_weight=0.25)
            self.assertEqual(score, expected_scores[b])

    def test_evaluate_4(self):

        expected_scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        game = Game()
        for b in range(0, 12):  # num_configs is the number of board configs you have
            config = getattr(board_configs, f'board_config{b + 1}')
            board = Board(config)
            score = evaluate(board, game, pieces_weight=0.0, kings_weight=0.0, moves_weight=0.0, opportunities_weight=0.0, king_hopefuls_weight=0.0)
            self.assertEqual(score, expected_scores[b])

    def test_minimax_alpha_beta_1(self):

        game = Game()
        board = Board()

        value, new_board = minimax_alpha_beta(board, 1, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config13)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_2(self):

        game = Game()
        board = Board()


        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config14)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_3(self):

        game = Game()
        board = Board()

        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game)

        true_board = Board(board_configs.board_config15)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_4(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 1, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config16)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_5(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config17)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_6(self):

        game = Game()
        board = Board()

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config18)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_7(self):

        game = Game()
        board = Board(board_configs.board_config1)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config19)

 
        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_8(self):

        game = Game()
        board = Board(board_configs.board_config2)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config20)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_9(self):

        game = Game()
        board = Board(board_configs.board_config3)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config21)
 

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_10(self):

        game = Game()
        board = Board(board_configs.board_config4)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)
        

        true_board = Board(board_configs.board_config22)
        


        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_11(self):

        game = Game()
        board = Board(board_configs.board_config6)

        eval_params = (0.0, 1.0, 1.0, 0.0, 0.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config23)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_12(self):

        game = Game()
        board = Board(board_configs.board_config7)

        eval_params = (1.0, 1.0, 0.5, 0.5, 0.25)
        value, new_board = minimax_alpha_beta(board, 2, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config24)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_13(self):

        game = Game()
        board = Board(board_configs.board_config9)

        eval_params = (1.0, 1.0, 0.0, 0.0, 1.0)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config25)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_14(self):

        game = Game()
        board = Board(board_configs.board_config10)

        eval_params = (0.0, 0.0, 0.0, 0.0, 0.0)
        value, new_board = minimax_alpha_beta(board, 4, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config26)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_15(self):

        game = Game()
        board = Board(board_configs.board_config11)

        eval_params = (1.0, 1.0, 1.5, 1.5, 1.25)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config27)

        self.assertTrue(compare_boards(new_board, true_board))

    def test_minimax_alpha_beta_16(self):

        game = Game()
        board = Board(board_configs.board_config12)

        eval_params = (1.0, 1.0, 1.0, 1.0, 1.0)
        value, new_board = minimax_alpha_beta(board, 3, float('-inf'), float('inf'), True, game, eval_params)

        true_board = Board(board_configs.board_config28)

        self.assertTrue(compare_boards(new_board, true_board))


tester = AiTest()

tester.test_minimax_alpha_beta_1()
print("TEST 1 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_2()
print("TEST 2 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_3()
print("TEST 3 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_4()
print("TEST 4 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_5()
print("TEST 5 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_6()
print("TEST 6 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_7()
print("TEST 7 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_8()
print("TEST 8 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_9()
print("TEST 9 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_10()
print("TEST 10 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_11()
print("TEST 11 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_12()
print("TEST 12 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_13()
print("TEST 13 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_14()
print("TEST 14 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_15()
print("TEST 15 PASSED: ++++++++++++++++++++++++++++++")
tester.test_minimax_alpha_beta_16()
print("TEST 16 PASSED: ++++++++++++++++++++++++++++++")

