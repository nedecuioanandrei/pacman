"""
This module contains all the logic for the Eight Puzzle game.
"""

from re import search
from typing import NamedTuple
from searchProblem import Successor, SearchProblem
import pandas as pd
from random import choice 
import os
import argparse


class IllegalMove(Exception):
    ...

class Point(NamedTuple):
    x: int
    y: int

class Offset(NamedTuple):
    dx: int
    dy: int 

class EightPuzzleSuccessor(Successor):
    position: Point 


class EightPuzzleGame():
    def __init__(self, size = None) -> None:
        if size is None:
            size = (3, 3)
        self.width, self.height = size
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]
        self.blackLocation = (0, 0)
        self.directionOffset = {
            'up': Offset(-1, 0),
            'down': Offset(1, 0),
            'left': Offset(0, -1),
            'right': Offset(0, 1)
        }
        self.initGame()

    def _getAsciiString(self):
        return str(pd.DataFrame(self.cells))

    def __str__(self):
        return self._getAsciiString()

    def __repr__(self):
        return 'size ({}:{})'.format(self.width, self.width)
    
    def _shuffle(self) -> None:
        for _ in range(3):
            self.doMove(choice(self.getLegalMoves())) 
    
    def _setInitialState(self) -> None:
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                self.cells[i][j] = count
                count += 1

    def initGame(self) -> None:
        self._setInitialState()
        self._shuffle()

    def isLegalMove(self, move) -> bool:
        return move in self.getLegalMoves()
    
    def getLegalMoves(self) -> list:
        moves = []
        row, col = self.blackLocation
        if row > 0:
            moves.append('up')
        if row < self.height - 1:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < self.width - 1:
            moves.append('right')
        return moves

    def doMove(self, move) -> None:
        if move not in self.directionOffset:
            raise ValueError('Unknown move name!')
        
        if not self.isLegalMove(move):
            raise IllegalMove
        
        oldRow, oldCol = self.blackLocation
        row = oldRow + self.directionOffset[move].dx
        col = oldCol + self.directionOffset[move].dy
        self.cells[row][col], self.cells[oldRow][oldCol] = self.cells[oldRow][oldCol], self.cells[row][col]
        self.blackLocation = (row, col)
    
    def isWin(self) -> bool:
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if count != self.cells[i][j]:
                    return False
                count += 1
        return True


class EightPuzzleProblem(SearchProblem):
    ...


def playEightPuzzleInConsole():
    g = EightPuzzleGame()
    while not g.isWin():
        os.system('clear')
        print(g)
        move = input('Next Move:\n')
        if move == 'q':
            raise SystemExit(0)
        try:
            g.doMove(move)
        except:
            ...
    print('WIIIIIIIIIIIIIIIIIIII')

def getParser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--play',action='store_true', help='Play the game in terminal.')
    group.add_argument('--test',action='store_true', help='The the algorithms.')
    return parser

if __name__ == '__main__':
    playEightPuzzleInConsole()


