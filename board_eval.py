import chess
import math

pVALS = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pawnValWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 45, 35,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]

pawnValBlack =  [0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 5, 0, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]




bishopValWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopValBlack = list(reversed(bishopValWhite))

knightVal = [
    -40, -30, -20, -20, -20, -20, -30, -40,
    -30, -10, 0, 5, 5, 0, -10, -30,
    -20, 5, 10, 15, 15, 10, 5, -20,
    -20, 0, 15, 20, 20, 15, 0, -20,
    -20, 5, 15, 20, 20, 15, 5, -20,
    -20, 0, 10, 15, 15, 10, 0, -20,
    -30, -10, 0, 0, 0, 0, -10, -30,
    -40, -30, -20, -20, -20, -20, -30, -40
]

rookValWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookValBlack = list(reversed(rookValWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))


def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
   
    if board.is_en_passant(move):
        return pVALS[chess.PAWN]
    
    _to = board.piece_at(move.to_square)
    _from = board.piece_at(move.from_square)
    if _to is None or _from is None:
        raise Exception(
            f"{move.to_square} and {move.from_square}"
        )
        
    if(board.turn == chess.WHITE):
        temp = chess.BLACK
    else:
        temp = chess.WHITE
    if len(board.attackers(temp, move.to_square)) >= 1:
        return pVALS[_to.piece_type] - pVALS[_from.piece_type]
    
    return pVALS[_to.piece_type]


def move_value(board: chess.Board, move: chess.Move, endgame: bool) -> float:
  
    if move.promotion is not None:
        return -float(math.inf) if board.turn == chess.BLACK else float(math.inf)

    _piece = board.piece_at(move.from_square)
    if _piece:
        from_value = evaluate_piece(_piece, move.from_square, endgame)
        to_value = evaluate_piece(_piece, move.to_square, endgame)
        position_change = to_value - from_value
    else:
        raise Exception(f"{move.from_square}")

    capturedValue = 0.0
    if board.is_capture(move):
        capturedValue = evaluate_capture(board, move)

    current_move_value = capturedValue + position_change
    if board.turn == chess.BLACK:
        current_move_value = -current_move_value

    return current_move_value



def evaluate_piece(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    
    piece_type = piece.piece_type
    mapping = []
    
    if piece_type == chess.KNIGHT:
        mapping = knightVal
    if piece_type == chess.PAWN:
        mapping = pawnValWhite if piece.color == chess.WHITE else pawnValBlack
    
    if piece_type == chess.ROOK:
        mapping = rookValWhite if piece.color == chess.WHITE else rookValBlack
    if piece_type == chess.BISHOP:
        mapping = bishopValWhite if piece.color == chess.WHITE else bishopValBlack
    if piece_type == chess.QUEEN:
        mapping = queenEval
    if piece_type == chess.KING:
        if end_game:
            mapping = (
                kingEvalEndGameWhite
                if piece.color == chess.WHITE
                else kingEvalEndGameBlack
            )
        else:
            mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    return mapping[square]


def evaluate_board(board: chess.Board) -> float:
 
    total = 0
    end_game = is_endgame(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        
        # imp = 1
        # if(piece.piece_type == chess.PAWN):
        #     imp = 1.5

        value = pVALS[piece.piece_type] + evaluate_piece(piece, square, end_game)
        total += value if piece.color == chess.WHITE else -value

    return total


def is_endgame(board: chess.Board) -> bool:
   
    queens = 0
    minors = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.QUEEN:
            queens += 1
        if piece and (
            piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT
        ):
            minors += 1

    if queens == 0 or (queens == 2 and minors <= 1):
        return True

    return False