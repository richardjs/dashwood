#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdbool.h>
#include <stdint.h>


#define MAX_ACTIONS 240


static uint64_t WIN_BOARDS[16][8];


static void initBitboards() {
    for (int space = 0; space < 16; space++) {
        for (int attribute = 0; attribute < 4; attribute++) {
            uint64_t attributeBits = 1 << attribute;

            uint64_t winboard = 0;
            int rowStart = (space / 4) * 4;
            for (int i = 0; i < 4; i++) {
                winboard |= attributeBits << (4 * (rowStart + i));
            }
            WIN_BOARDS[space][attribute] = winboard;

            winboard = 0;
            int colStart = space % 4;
            for (int i = 0; i < 4; i++) {
                winboard |= attributeBits << (4 * (colStart + 4*i));
            }
            WIN_BOARDS[space][attribute + 4] = winboard;
        }
    }
}


static struct State {
    uint64_t	board;
    uint64_t	iboard;
    uint8_t	nextPiece;
    uint16_t	usedPieces;
    uint8_t	lastSpace;
};


static struct Action {
    uint8_t space;
    uint8_t piece;
};


static void State_initial(struct State *state) {
    state->board = 0;
    state->iboard = 0;
    state->nextPiece = 0;
    state->usedPieces = 1;
    state->lastSpace = 0;
}


static void State_move(struct State *state, const struct Action *action) {
    uint8_t spaceOffset = action->space * 4;
    state->board |= (uint64_t)state->nextPiece << spaceOffset;
    state->iboard |= (uint64_t)(~state->nextPiece & 0b1111) << spaceOffset;
    state->nextPiece = action->piece;
    state->usedPieces |= 1 << action->piece;
    state->lastSpace = action->space;
}


static int State_actions(const struct State *state, struct Action actions[]){
    uint64_t filledBits = state->board | state->iboard;

    int count = 0;
    for (uint8_t space = 0; space < 16; space++) {
        if (filledBits & (0b1111llu << (4*space))) {
            continue;
        }

        for (uint8_t piece = 0; piece < 16; piece++){
            if (state->usedPieces & (1 << piece)) {
                continue;
            }
            actions[count].space = space;
            actions[count++].piece = piece;
        }
    }
    return count;
}


static bool State_isWin(const struct State *state) {
    for (int i = 0; i < 8; i++) {
        if ((WIN_BOARDS[state->lastSpace][i] & state->board) == WIN_BOARDS[state->lastSpace][i]) {
            return true;
        }
        if ((WIN_BOARDS[state->lastSpace][i] & state->iboard) == WIN_BOARDS[state->lastSpace][i]) {
            return true;
        }
    }
    return false;
}


/* Build a complete State from only what we technically need. */
static void State_from(struct State *state,
	uint64_t board, uint64_t iboard, uint8_t nextPiece) {
    state->board = board;
    state->iboard = iboard;
    state->nextPiece = nextPiece;

    state->usedPieces = 1 << nextPiece;
    for (int space = 0; space < 16; space++) {
	int piece = (board >> (4*space)) & 0b1111;
	if (piece) {
	    state->usedPieces |= 1 << piece;
	} else {
	    int ipiece = (iboard >> (4*space)) & 0b1111;
	    if (ipiece == 0b1111) {
		state->usedPieces |= 1;
	    }
	}
    }

    // If there's a win on the board, we'll assume one of its spaces was
    // the last move. If not, it doesn't really matter, so we'll just
    // arbitrarily set lastSpace to a filled space.
    state->lastSpace = 0;
    uint64_t filledBits = state->board | state->iboard;
    for (int space = 0; space < 16; space++) {
	if ((filledBits >> space) & 0b1111 == 0){
	    continue;
	}
	state->lastSpace = space;
	if (State_isWin(&state)) {
	    break;
	}
    }
}


static void State_print(const struct State *state) {
    fprintf(stderr, "---\n");
    fprintf(stderr, "board:\t\t%d\t%x\n", state->board, state->board);
    fprintf(stderr, "iboard:\t\t%d\t%x\n", state->iboard, state->iboard);
    fprintf(stderr, "nextPiece:\t%d\t%x\n", state->nextPiece, state->nextPiece);
    fprintf(stderr, "usedPieces:\t%d\t%x\n", state->usedPieces, state->usedPieces);
    fprintf(stderr, "lastSpace:\t%d\t%x\n", state->lastSpace, state->lastSpace);
    fprintf(stderr, "---\n");
}


static double negamax(const struct State *state, int depth){
    if (State_isWin(state)) {
        return -1.0;
    }
    if (depth == 0) {
        return 0.0;
    }

    double bestScore = -1.0;
    struct Action actions[MAX_ACTIONS];
    int count = State_actions(state, actions);
    for (int i = 0; i < count; i++) {
        struct State child = *state;
        State_move(&child, &actions[i]);
        double score = -negamax(&child, depth - 1);
        if (score > bestScore) {
            bestScore = score;
        }
    }
    return bestScore;
}


static PyObject *c_minimax(PyObject *self, PyObject *args) {
    uint64_t board, iboard;
    uint8_t nextPiece;
    int depth;
    if (!PyArg_ParseTuple(args, "(kkb)i", &board, &iboard, &nextPiece, &depth)) {
	return NULL;
    }

    struct State state;
    State_from(&state, board, iboard, nextPiece);

    double score = negamax(&state, depth);
    return PyFloat_FromDouble(score);
}


static PyMethodDef CMethods[] = {
    {"minimax", c_minimax, METH_VARARGS, "Score a state with minimax."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef cmodule = {
    PyModuleDef_HEAD_INIT,
    "c",
    NULL,
    -1,
    CMethods
};


PyMODINIT_FUNC PyInit_c(void) {
    initBitboards();
    return PyModule_Create(&cmodule);
}
