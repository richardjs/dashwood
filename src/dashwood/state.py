'''State representation and operations

The most basic state representation is a 3-tuple, defined as:
    [0] pieces on board
    [1] inverse of pieces on board
    [2] the next piece to be placed

[1] is not ~[0]. Rather, it is the inverse of the *pieces* on the board.
The inverse calculation is performed when the piece is ORed onto the
bitboard in move(). Note this means piece 0b0000, while
indistinguishable from empty space on [0], is 0b1111 on [1].

Board space numbering:
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
'''


from dashwood import bitboards
from dashwood.c import minimax


class State():
    def __init__(self, state_tuple=(0, 0, 0)):
        board, iboard, next_piece = state_tuple
        self.board = board
        self.iboard = iboard
        self.next_piece = next_piece

        self.pieces_left = set(range(16))
        self.pieces_left.remove(next_piece)
        for space in range(16):
            piece = (board >> (space*4)) & 0b1111
            if piece:
                self.pieces_left.remove(piece)
            else:
                ipiece = (iboard >> (space*4)) & 0b1111
                if piece == 0b1111:
                    self.pieces_left.remove(0)

    @property
    def tuple(self):
        return (self.board, self.iboard, self.next_piece)

    @property
    def actions(self):
        filled_bits = self.board | self.iboard
        for space in range(16):
            space_bits = 0b1111 << (4*space)
            if filled_bits & space_bits:
                continue

            for next_piece in self.pieces_left:
                yield (space, next_piece)

    @property
    def is_win(self):
        for space in range(16):
            for winboard in bitboards.wins[space]:
                if (self.board & winboard) == winboard:
                    return True
                if (self.iboard & winboard) == winboard:
                    return True

        return False

    def minimax(self, depth):
        return minimax(self.tuple, depth)

    def move(self, action):
        space, next_piece = action
        self.board |= (self.next_piece << (4*space))
        self.iboard |= ((~self.next_piece & 0b1111) << (4*space))
        self.next_piece = next_piece
        self.pieces_left.remove(next_piece)

    def __str__(self):
        return ' '.join([bin(self.board), bin(self.iboard), bin(self.next_piece)])

    def __repr__(self):
        return self.__str__()
