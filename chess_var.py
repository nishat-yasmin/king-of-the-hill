# Author: Nishat Yasmin
# GitHub username: nishat-yasmin
# Date: 03/16/2025
# Description: A program that implements a "King of the Hill" variant of a
#              chess game.

class ChessVar:
    """A class to implement an abstract board game based on a 'King of the
    Hill' chess variant. White always moves first; there is no check,
    checkmate, castling, en passant, or pawn promotion; the game ends when
    either the opponent's king is captured or one player's king is brought
    to one of the four central squares of the board.
    """

    def __init__(self):
        """Constructor for ChessVar class.Takes no parameters and initializes
        the private data members: board, game_state, and current_turn.
        """

        self._board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        self._game_state = "UNFINISHED"
        self._curr_turn = "WHITE"

    def get_game_state(self):
        """Returns game state: 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'."""
        return self._game_state

    def get_board(self):
        """Returns the current board as a nested list."""
        return self._board

    def make_move(self, from_square, to_square):
        """Takes as parameters two spaces on the board. Returns
        False if the game state is not "UNFINISHED", the from_square
        is empty, or it is not valid for the piece to move to to_square.
        Otherwise, updates board by moving piece from from_square to
        to_square, updates game_state, updates current_turn, and returns True.
        """

        # Check if the game is over.
        if self._game_state != "UNFINISHED":
            return False

        # Check algebraic notation is valid.
        if from_square[0] not in "abcdefgh" or to_square[0] not in "abcdefgh":
            return False
        if from_square[1] not in "12345678" or to_square[1] not in "12345678":
            return False
        if len(from_square) != 2 or len(to_square) != 2:
            return False

        # Convert algebraic notation of piece to index.
        from_row, from_col = algebra_to_index(from_square)
        to_row, to_col = algebra_to_index(to_square)
        curr_piece = self._board[from_row][from_col]

        # Check if current piece is empty.
        if curr_piece == " ":
            return False

        # Check if current piece matches current turn.
        if self._curr_turn == "WHITE" and curr_piece.islower():
            return False
        if self._curr_turn == "BLACK" and curr_piece.isupper():
            return False

        # Check if desired move is valid for the current piece.
        if not self.is_valid(from_row, from_col, to_row, to_col):
            return False

        # Move current piece, store captured piece if any.
        capt_piece = self._board[to_row][to_col]
        self._board[to_row][to_col] = curr_piece
        self._board[from_row][from_col] = " "

        # Check if current piece is king that has moved to a central square.
        if (to_row, to_col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
            if curr_piece == "k":
                self._game_state = "BLACK_WON"
                return True
            if curr_piece == "K":
                self._game_state = "WHITE_WON"
                return True

        # Check if captured piece is a king.
        if capt_piece == "K":
            self._game_state = "BLACK_WON"
            return True
        if capt_piece == "k":
            self._game_state = "WHITE_WON"
            return True

        # Else, change turns.
        if self._curr_turn == "WHITE":
            self._curr_turn = "BLACK"
        else:
            self._curr_turn = "WHITE"

        return True

    def is_valid(self, from_row, from_col, to_row, to_col):
        """Takes as parameters a piece's current position
        (from_row, from_col) and its target position (to_row, to_col),
        and determines whether such a move would be allowed for that
        piece type. Includes logic to account for the movement rules
        of each piece, and will call the is_clear method for sliding
        pieces. Returns True if the move is valid, otherwise False.
        """

        # Check current and target positions are on the board.
        if not (0 <= from_row < 8 and 0 <= from_col < 8):
            return False
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        curr_pos = self._board[from_row][from_col]
        target_pos = self._board[to_row][to_col]

        # If piece will be captured, check it isn't current player's own piece.
        if target_pos != " ":
            if curr_pos.isupper() and target_pos.isupper():
                return False
            if curr_pos.islower() and target_pos.islower():
                return False

        # Check if move is valid for that piece type:
        piece_type = curr_pos
        if piece_type == "p" or piece_type == "P":
            return self.is_valid_pawn(from_row, from_col, to_row, to_col)
        if piece_type == "r" or piece_type == "R":
            return self.is_valid_rook(from_row, from_col, to_row, to_col)
        if piece_type == "n" or piece_type == "N":
            return self.is_valid_knight(from_row, from_col, to_row, to_col)
        if piece_type == "b" or piece_type == "B":
            return self.is_valid_bishop(from_row, from_col, to_row, to_col)
        if piece_type == "q" or piece_type == "Q":
            return self.is_valid_queen(from_row, from_col, to_row, to_col)
        if piece_type == "k" or piece_type == "K":
            return self.is_valid_king(from_row, from_col, to_row, to_col)
        return False

    def is_clear(self, from_row, from_col, to_row, to_col):
        """Takes as parameters a piece's current position
        (from_row, from_col) and its target position (to_row, to_col),
        and determines whether each square along the path is empty. This
        is relevant in determining the validity of moves of sliding pieces
        (queen, bishop, rook). Returns True if the path is clear, else False.
        """

        row_direction = 0
        if to_row > from_row:  # moving downward
            row_direction = 1
        elif to_row < from_row:  # moving upward
            row_direction = -1

        col_direction = 0
        if to_col > from_col:  # moving rightward
            col_direction = 1
        elif to_col < from_col:  # moving leftward
            col_direction = -1

        # Check each square on the way to the target square is empty.
        curr_row = from_row + row_direction
        curr_col = from_col + col_direction
        while curr_row != to_row or curr_col != to_col:
            if self._board[curr_row][curr_col] != " ":
                return False
            curr_row += row_direction
            curr_col += col_direction

        return True

    def is_valid_pawn(self, from_row, from_col, to_row, to_col):
        """Determines whether pawn can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        curr_pos = self._board[from_row][from_col]
        target_pos = self._board[to_row][to_col]

        if curr_pos.isupper():  # if pawn is white
            direction = -1      # only move up (decreasing index)
            init_row = 6        # game start position is row 6
        else:                   # if pawn is black
            direction = 1       # only move down (increasing index)
            init_row = 1        # game start position is row 1

        # Pawn has option to move forward 2 squares from its starting position.
        if from_col == to_col:
            if from_row == init_row:
                if to_row == from_row + (2*direction):
                    if self.is_clear(from_row, from_col, to_row, to_col):
                        if target_pos == " ":
                            return True

        # Else, pawn may only move forward 1 space at a time.
        if from_col == to_col:
            if to_row == from_row + direction:
                if target_pos == " ":  # pawn not allowed to capture forward
                    return True

        # Pawn may move diagonally only to capture a piece.
        if abs(to_col - from_col) == 1:
            if to_row == from_row + direction:
                if target_pos != " ":
                    return True

        # Else, invalid.
        return False

    def is_valid_rook(self, from_row, from_col, to_row, to_col):
        """Determines whether rook can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        # Rook can slide vertically or horizontally but not both.
        if from_row != to_row and from_col != to_col:
            return False

        if from_row == to_row and from_col == to_col:
            return False

        # Check path to target position is clear.
        return self.is_clear(from_row, from_col, to_row, to_col)

    def is_valid_knight(self, from_row, from_col, to_row, to_col):
        """Determines whether knight can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        # Knight can move 1 vertically + 2 horizontally or vice versa.
        if abs(to_row - from_row) == 1 and abs(to_col - from_col) == 2:
            return True
        if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 1:
            return True
        return False

    def is_valid_bishop(self, from_row, from_col, to_row, to_col):
        """Determines whether bishop can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        # Bishop can slide diagonally only.
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False

        # Check path to target position is clear.
        return self.is_clear(from_row, from_col, to_row, to_col)

    def is_valid_queen(self, from_row, from_col, to_row, to_col):
        """Determines whether queen can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        # Queen can slide like the rook or the bishop.
        return (self.is_valid_rook(from_row, from_col, to_row, to_col) or
                self.is_valid_bishop(from_row, from_col, to_row, to_col))

    def is_valid_king(self, from_row, from_col, to_row, to_col):
        """Determines whether king can be moved from its current position
        (from_row, from_col) to the target position (to_row, to_col). Returns
        True if valid, else False.
        """

        if abs(to_row - from_row) <= 1:
            if abs(to_col - from_col) <= 1:
                return True
        return False


def algebra_to_index(square):
    """Takes as parameter a string (e.g. "a1") representing the algebraic
    notation of a square on the board and returns it as a tuple of the
    corresponding row, col.
    """

    letter = square[0]
    number = square[1]

    letter_conversion = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5,
                         "g": 6, "h": 7}

    col = letter_conversion[letter]

    number_conversion = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5,
                         "2": 6, "1": 7}

    row = number_conversion[number]

    return (row, col)


def main():
    game = ChessVar()
    print(game.make_move('d2', 'd4'))
    print(game.make_move('g7', 'g5'))
    print(game.make_move('c1', 'g5'))
    print(game.make_move('e7', 'e6'))
    print(game.make_move('g5', 'd8'))
    print(game.get_board())


if __name__ == "__main__":
    main()
