from typing import Dict, List, Any
import chess as ch
import sys
import time
from board_eval import evaluate_board, move_value, is_endgame
import math
SCORE_MATE     = 1000000000
THRESHOLD =  999000000


debug_info: Dict[str, Any] = {}



def next_move(board:ch.Board, depth:int = 3, debug=True)->ch.Move:
    
    debug_info.clear()
    debug_info["nodes"] = 0
    t = time.time()

    move = mm_root(depth, board)

    debug_info["time"] = time.time() - t
    if(debug):
        print(f"info {debug_info}")
    return move


def get_ordered_moves(board: ch.Board) -> List[ch.Move]:
    
    end_game = is_endgame(board)

    def orderer(move):
        return move_value(board, move, end_game)

    sorted_moves = sorted(board.legal_moves, key=orderer, reverse=(board.turn == ch.WHITE))
    return list(sorted_moves)


def mm_root(depth: int, board: ch.Board) -> ch.Move:
    maximize = (board.turn == ch.WHITE)
    best_move = -float(math.inf)
    if not maximize:
        best_move = float(math.inf)

    moves = get_ordered_moves(board)
    best_result = moves[0]

    for options in moves:
        board.push(options)

        if(board.can_claim_draw()):
            value = 0.00
        else:
            value = minimax(depth - 1, board, -float(math.inf), float(math.inf), not maximize)

        board.pop()

        if(maximize):
            if(value >= best_move):
                best_move = value
                best_result = options
        else: 
            if(value <= best_move):
                best_move = value
                best_result = options

    return best_result


def minimax(depth: int, board: ch.Board,alpha: float, beta: float, my_player: bool) -> float:
    debug_info["nodes"] += 1

    if (board.is_checkmate()):
        
        return -SCORE_MATE if my_player else SCORE_MATE
   
    elif (board.is_game_over()):
        return 0

    if (depth == 0):
        return evaluate_board(board)

    if (my_player == True):
        
        options = get_ordered_moves(board)

        best_move = -float(math.inf)

        for option in options:
            board.push(option)
            current_choice = minimax(depth - 1, board, alpha, beta, not my_player)
         
            if current_choice > THRESHOLD:
                current_choice -= 1
            elif current_choice < -THRESHOLD:
                current_choice += 1
            best_move = max(best_move, current_choice)
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    
    else:
        best_move = float(math.inf)

        moves = get_ordered_moves(board)

        for move in moves:
            board.push(move)
            current_choice = minimax(depth - 1, board, alpha, beta, not my_player)

            if (current_choice > THRESHOLD):
                current_choice -= 1
            elif (current_choice < -THRESHOLD):
                current_choice += 1

            best_move = min(best_move,current_choice)
            board.pop()
            beta = min(beta, best_move)

            if(alpha >= beta):
                return best_move
            

        return best_move