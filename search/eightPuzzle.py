"""
This module contains all the logic for the Eight Puzzle game.
"""

from searchProblem import SearchProblem
from searchImplementations import *
from typing import NamedTuple
from random import choice
from functools import total_ordering
import pandas as pd
import argparse
import copy
import sys
import os


class IllegalMove(Exception):
    ...


class InvalidBoard(Exception):
    ...


class Offset(NamedTuple):
    dx: int
    dy: int


class EightPuzzleGame:
    def __init__(self, size=None, shuffle_steps=100) -> None:
        if size is None:
            size = (3, 3)
        self.shuffle_steps = shuffle_steps
        self.height, self.width = size
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]
        self.blackLocation = (0, 0)
        self.directionOffset = {
            "up": Offset(-1, 0),
            "down": Offset(1, 0),
            "left": Offset(0, -1),
            "right": Offset(0, 1),
        }
        self.initGame()

    def _getAsciiString(self):
        return str(pd.DataFrame(self.cells))

    def __str__(self):
        return self._getAsciiString()

    def __repr__(self):
        return "size ({}:{})\n{}".format(self.width, self.width, self._getAsciiString())

    def _shuffle(self) -> None:
        for _ in range(self.shuffle_steps):
            self.doMove(choice(self.getLegalMoves()))

    def _setInitialState(self) -> None:
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j] = count
                count += 1

    def initGame(self) -> None:
        self._setInitialState()
        self._shuffle()

    def getState(self):
        return self.cells

    def isLegalMove(self, move) -> bool:
        return move in self.getLegalMoves()

    def getLegalMoves(self) -> list:
        moves = []
        row, col = self.blackLocation
        if row > 0:
            moves.append("up")
        if row < self.height - 1:
            moves.append("down")
        if col > 0:
            moves.append("left")
        if col < self.width - 1:
            moves.append("right")
        return moves

    def doMove(self, move) -> None:
        if move not in self.directionOffset:
            raise ValueError("Unknown move name!")

        if not self.isLegalMove(move):
            raise IllegalMove

        oldRow, oldCol = self.blackLocation
        row = oldRow + self.directionOffset[move].dx
        col = oldCol + self.directionOffset[move].dy
        self.cells[row][col], self.cells[oldRow][oldCol] = (
            self.cells[oldRow][oldCol],
            self.cells[row][col],
        )
        self.blackLocation = (row, col)

    def isWin(self) -> bool:
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if count != self.cells[i][j]:
                    return False
                count += 1
        return True


@total_ordering
class EightPuzzleState:
    def __init__(self, configuration):
        self.cells = configuration
        self.width = len(configuration[0])
        self.height = len(configuration)
        self.blank_space_position = None
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] == 0:
                    self.blank_space_position = (i, j)
        self.directionOffset = {
            "up": Offset(-1, 0),
            "down": Offset(1, 0),
            "left": Offset(0, -1),
            "right": Offset(0, 1),
        }

    def __eq__(self, other):
        return str(other) == self._getAsciiString()

    def __lt__(self, other):
        return False

    def __hash__(self):
        return hash(str(self))

    def _getAsciiString(self):
        return str(pd.DataFrame(self.cells))

    def __str__(self):
        return self._getAsciiString()

    def __repr__(self):
        return self._getAsciiString()

    def isGoal(self):
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if count != self.cells[i][j]:
                    return False
                count += 1
        return True

    def applyMove(self, move):
        if move not in self.getLegalMoves():
            raise IllegalMove
        oldRow, oldCol = self.blank_space_position
        row = oldRow + self.directionOffset[move].dx
        col = oldCol + self.directionOffset[move].dy
        cp = copy.deepcopy(self.cells)
        try:
            cp[row][col], cp[oldRow][oldCol] = (cp[oldRow][oldCol], cp[row][col])
        except:
            print(row, col)
            print(oldRow, oldCol)
            raise
        return cp

    def getLegalMoves(self):
        if self.blank_space_position is None:
            raise InvalidBoard
        moves = []
        row, col = self.blank_space_position
        if row > 0:
            moves.append("up")
        if row < self.height - 1:
            moves.append("down")
        if col > 0:
            moves.append("left")
        if col < self.width - 1:
            moves.append("right")
        return moves

    def getCells(self):
        return self.cells

    def getSize(self):
        return self.height, self.width


class EightPuzzleProblem(SearchProblem):
    def __init__(self, size=None, shuffle_steps=100):
        self.directionOffset = {
            "up": Offset(-1, 0),
            "down": Offset(1, 0),
            "left": Offset(0, -1),
            "right": Offset(0, 1),
        }
        if size is None:
            size = (3, 3)
        self.height, self.width = size
        tmp = EightPuzzleGame(size=size, shuffle_steps=shuffle_steps)
        self.initialState = EightPuzzleState(tmp.getState())

    def __str__(self):
        return str(self.initialState)

    def __repr__(self):
        return str(self)

    def getStartState(self):
        return self.initialState

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        return [
            (EightPuzzleState(state.applyMove(move)), move, 1)
            for move in state.getLegalMoves()
        ]

    def getCostOfActions(self, actions) -> int:
        return len(actions)


def playEightPuzzleInConsole(args):
    g = EightPuzzleGame()
    unknown_move = False
    while not g.isWin():
        os.system("clear")
        if unknown_move:
            print("Last move was an unknown move!")
        unknown_move = False
        print(g)
        move = input("Next Move (up, down, left, right):\n").strip()
        if move == "q":
            raise SystemExit(0)
        try:
            g.doMove(move)
        except:
            unknown_move = True
    print("We have a winner!")


def test(args):
    function_mapping = {"dfs": dfsSearch, "bfs": bfsSearch, "astar": aStarSearch}
    heuritic_mapping = {
        "none": nullHeuristic,
        "manh": manhattanDistHeuristic,
        "pos": outOfPosHeuristic,
    }
    if args.search_function not in function_mapping:
        raise ValueError("Method is not implemented!")
    average_iterations = 0
    average_state_count = 0
    for index in range(args.test_case_count):
        p = EightPuzzleProblem(
            (args.height, args.width), shuffle_steps=args.shuffle_steps
        )
        print("Test case number #{}".format(index + 1))
        print(p, "\n")
        output, searched_states = function_mapping[args.search_function](
            p, heuristic=heuritic_mapping[args.heuristic]
        )
        iterations_for_this_test_case = p.getCostOfActions(output)
        print("Score :{}\n".format(int(iterations_for_this_test_case)))
        print("Searched_states :{}\n".format(searched_states))
        average_iterations += iterations_for_this_test_case / args.test_case_count
        average_state_count += searched_states / args.test_case_count
    print("Average number of iterations :{}".format(average_iterations))
    print("Average number of searched states :{}".format(average_state_count))


def getParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="actions")
    play_parser = subparsers.add_parser("play")
    play_parser.set_defaults(func=playEightPuzzleInConsole)

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("--width", default=3, type=int)
    test_parser.add_argument("--height", default=3, type=int)
    test_parser.add_argument("--shuffle-steps", default=3, type=int)
    test_parser.add_argument("--test-case-count", default=1, type=int)
    test_parser.add_argument("--search-function", default="bfs")
    test_parser.add_argument("--heuristic", default="none")
    test_parser.set_defaults(func=test)
    return parser


if __name__ == "__main__":
    parser = getParser()
    args = parser.parse_args(sys.argv[1:])
    args.func(args)
    raise SystemExit(0)
