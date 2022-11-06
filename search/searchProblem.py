"""
This module contains the base class for a search problem.
"""
from typing import List, NamedTuple, Any
from abc import ABC as AbstractClass


class Successor(NamedTuple):
    """
    A search problem successor.
    """
    position: Any
    action: str
    cost: int


class SearchProblem(AbstractClass):
    """
    This class serves as a blueprint for a search problem.
    """
    def getStartState(self) -> None:
        """
        This function must return the start state of the search problem.
        """
        raise NotImplemented

    def isGoalState(self, state) -> None:
        """
        This function returns True if the state is the goal state and False otherwise.
        """
        raise NotImplemented

    def getSuccessors(self, state) -> List:
        """
        For a given state this function will return a list of named tuples
            (position, action, cost)
        """
        raise NotImplemented

    def getCostOfActions(self, actions) -> int:
        """
        This method will retrieve the cost of a sequence of actions.
        """
        raise NotImplemented


