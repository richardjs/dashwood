#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>


#define MAX_ACTIONS 240


uint64_t WIN_BOARDS[16][8];


void initBitboards() {
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


struct State {
    uint64_t	board;
    uint64_t	iboard;
    uint8_t	nextPiece;
    uint16_t	usedPieces;
    uint8_t	lastSpace;
};


struct Action {
    uint8_t space;
    uint8_t piece;
};


void State_init(struct State *state) {
    state->board = 0;
    state->iboard = 0;
    state->nextPiece = 0;
    state->usedPieces = 1;
    state->lastSpace = 0;
}


void State_move(struct State *state, const struct Action *action) {
    uint8_t spaceOffset = action->space * 4;
    state->board |= (uint64_t)state->nextPiece << spaceOffset;
    state->iboard |= (uint64_t)(~state->nextPiece & 0b1111) << spaceOffset;
    state->nextPiece = action->piece;
    state->usedPieces |= 1 << action->piece;
    state->lastSpace = action->space;
}


int State_actions(const struct State *state, struct Action actions[]){
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


bool State_isWin(const struct State *state) {
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


double negamax(const struct State *state, int depth){
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


int main() {
    initBitboards();

    struct State state;
    State_init(&state);
    printf("%f\n", negamax(&state, 3));

    return 0;
}
