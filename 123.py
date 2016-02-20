#!/usr/bin/env python
# -*- coding: utf-8 -*-


# SOURCE: https://habrahabr.ru/post/140581/

import itertools

def neigbors(point):
    x, y = point
    for i, j in itertools.product(range(-1, 2), repeat=2):
        if any((i, j)):
            yield (x + i, y + j)

def advance(board):
    newstate = set()
    recalc = board | set(itertools.chain(*map(neigbors, board)))
    for point in recalc:
        count = sum((neigh in board) for neigh in neigbors(point))
        if count == 3 or (count == 2 and point in board):
            newstate.add(point)

    return newstate

glider = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
glider = set([(0, 1), (1, 1), (2, 1)])

# n = 5
# glider = set([(0, 1), (1, 1), (2, 1), (0 + n, 1 + n), (1 + n, 1 + n), (2 + n, 1 + n)])
# for i in range(1000):
#     glider = advance(glider)
#     print(glider)
#
# print(list(itertools.product(range(-1, 2), repeat=2)))

print(list(neigbors((0, 0))))
print([list(i) for i in list(map(neigbors, glider))])
print(list(itertools.chain(*[list(i) for i in list(map(neigbors, glider))])))
print(set(itertools.chain(*[list(i) for i in list(map(neigbors, glider))])))

# glider = advance(glider)
# print(glider)