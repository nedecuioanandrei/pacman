from dataStructures import *
from queue import Queue, PriorityQueue
import pandas as pd


def nullHeuristic(state=None, problem=None):
    return 0


def manhattanDistHeuristic(state=None, problem=None):
    if None in (state, problem):
        return 0
    dist = 0
    cells = state.getCells()
    height, width = state.getSize()
    for i in range(height):
        for j in range(width):
            shi = cells[i][j] / width
            shj = cells[i][j] % width
            dist += abs(i - shi) + abs(j - shj)
    return dist


def outOfPosHeuristic(state=None, problem=None):
    if None in (state, problem):
        return 0
    dist = 0
    cells = state.getCells()
    height, width = state.getSize()
    count = 0
    for i in range(height):
        for j in range(width):
            if count != cells[i][j]:
                dist += 1
            count += 1
    return dist * 0.7 + manhattanDistHeuristic(state=state, problem=problem) * 0.3


def dfsSearch(problem, **kwargs):
    searched_states = 1
    stack = Stack()
    stack.push(problem.getStartState())
    visited = []
    parent = {}

    while not stack.isEmpty():
        current = stack.pop()
        visited.append(current)
        if problem.isGoalState(current):
            node = current
            path = []
            while node != problem.getStartState:
                path.append(parent[node])
                node = parent[node][0]
            return ([x for (_, x) in reversed(path)], searched_states)
        for neighbour, direction, _ in problem.getSuccessors(current):
            if neighbour not in visited:
                searched_states += 1
                parent[neighbour] = (current, direction)
                stack.push(neighbour)
    return ([], searched_states)


def bfsSearch(problem, **kwargs):
    searched_states = 1
    q = Queue()
    q.put(problem.getStartState())
    visited = []
    parent = {}

    while not q.empty():
        current = q.get()
        visited.append(current)
        if problem.isGoalState(current):
            node = current
            path = []
            while node != problem.getStartState():
                path.append(parent[node])
                node = parent[node][0]
            return ([x for (_, x) in reversed(path)], searched_states)
        for neighbour, direction, _ in problem.getSuccessors(current):
            if neighbour not in visited:
                searched_states += 1
                parent[neighbour] = (current, direction)
                q.put(neighbour)
    return ([], searched_states)


def aStarSearch(problem, heuristic=nullHeuristic):
    searched_states = 1
    q = PriorityQueue()
    q.put((heuristic(problem.getStartState(), problem), problem.getStartState()))
    visited = []
    parent = {}

    while not q.empty():
        prio, current = q.get()
        visited.append(current)
        if problem.isGoalState(current):
            node = current
            path = []
            while node != problem.getStartState():
                path.append(parent[node])
                node = parent[node][0]
            return ([x for (_, x) in reversed(path)], searched_states)
        for neighbour, direction, _ in problem.getSuccessors(current):
            if neighbour not in visited:
                searched_states += 1
                parent[neighbour] = (current, direction)
                q.put((heuristic(neighbour, problem), neighbour))
    return ([], searched_states)
