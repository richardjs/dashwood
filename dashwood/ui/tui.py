from sys import stdout

# PIECE_STRINGS[16] is the string for empty space
PIECE_STRINGS = [
    'abcd',
    'abcD',
    'abCd',
    'abCD',
    'aBcd',
    'aBcD',
    'aBCd',
    'aBCD',
    'Abcd',
    'AbcD',
    'AbCd',
    'AbCD',
    'ABcd',
    'ABcD',
    'ABCd',
    'ABCD',
    '....',
]


def print_state(state):
    for i in range(16):
        piece = (int(state[0]) >> (4*i)) & 0b1111

        # determine if this is piece 0b0000 or empty space
        if piece == 0:
            if (int(state[1]) >> (4*i)) & 0b1111 == 0:
                piece = 16

        if (i + 1) % 4 != 0:
            stdout.write(f'{PIECE_STRINGS[piece]} ')
        else:
            stdout.write(f'{PIECE_STRINGS[piece]}\n')
