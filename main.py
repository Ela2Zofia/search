"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import math
from collections import defaultdict

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing
from queue import PriorityQueue

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)
    
    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information)

    board_dict = defaultdict(list)
    upper = defaultdict(list)
    lower = defaultdict(list)
    target = defaultdict(list)
    block = []
    turn = 1

    board = generate_board()

    # preparation of the data
    for category in data:
        for token in data[category]:
            if token:
                if category == "upper":
                    board_dict[(token[1], token[2])].append( "(" + token[0].upper()   + ")" )
                    upper[(token[1], token[2])].append(token[0])
                else:
                    board_dict[(token[1], token[2])].append( "(" + token[0] + ")" )
                    if category == "lower":
                        board_dict[(token[1], token[2])].append(token[0])
                    elif category == "block":
                        block.append((token[1], token[2]))

    for i in upper.keys():
        for j in lower.keys():
            if defeat(upper[i], lower[j]):
                target[i].append(j)

    finished = False
    while not finished:
        finished = True

        for i in upper.keys():
            frontier = PriorityQueue()

            tar = target[i][0]
            
            # if target[i]:
            #     tar = target[i][0]
            # else:
            #     tar = 
            
            frontier.put((0, i))
            cost_dict = {}
            path = []
            come_from = {}
            cost_dict[i] = 0

            while not frontier.empty():
                current = frontier.get()
                neighbours = []
                if current == tar:
                    break

                # calculate distance to the target as a basic heuristic metric
                for neighbour in board[current]:
                    if neighbour not in block:
                        neighbours.append(neighbour)
                        
                # check if swing is possible
                for other in upper.keys():
                    if distance(other, current) == 1:
                        for neighbour in board[other]:
                            if distance(neighbour, current) > 1:
                                neighbours.append(neighbour)

                # add node to priority queue if it is not yet there or there is a shorter route already
                for neighbour in neighbours:
                    cost = cost_dict[current] + 1
                    if neighbour not in cost_dict.keys() or cost < cost_dict[cost]:
                        cost_dict[neighbour] = cost
                        come_from[neighbour] = current
                        frontier.put((cost + distance(tar, neighbour), neighbour))
            
            # get the path from target back to start
            # path tracking implementation inspired by https://www.redblobgames.com/pathfinding/a-star/implementation.html
            while come_from[tar] != i:
                path.append(come_from[tar])
                tar = come_from[tar]
            
            # we only care about the first step of the moves
            move_to = path[-1]
            
            # TODO: game rule check if the block we move into conatin any defeats

            board_dict[move_to] = board_dict[i]
            board_dict.pop(i)

            upper[move_to] = upper[i]
            upper.pop(i)



            if distance(i, move_to) > 1:
                print_swing(turn, i[0], i[1], move_to[0], move_to[1])
            else:
                print_slide(turn, i[0], i[1], move_to[0], move_to[1])
        

        if lower:
            finished = False
        turn += 1
        

    
    # print_board(board_dict, compact=False)

# def heuristics(upper, token, target):

def distance(first, second):
    return (abs(first[1] - second[1]) + abs(first[1] - second[1] + first[0] - second[0]) + abs(first[0] - second[0])) / 2

def defeat(first, second):
    f = first.lower()
    s = second.lower()
    if f == "r":
        if s == "r":
            return False
        elif s == "p":
            return False
        elif s == "s":
            return True
    elif f == "p":
        if s == "r":
            return True
        elif s == "p":
            return False
        elif s == "s":
            return False
    elif f == "s":
        if s == "r":
            return False
        elif s == "p":
            return True
        elif s == "s":
            return False
    else:
        return False

def generate_board():
    board = defaultdict(list)
    ran = range(-3, 4)
    for r,q in [(r,q) for r in ran for q in ran if -r-q in ran]:
        board[(r,q)].append((r,q+1))
        board[(r,q)].append((r,q-1))
        board[(r,q)].append((r+1,q))
        board[(r,q)].append((r-1,q))
        board[(r,q)].append((r+1,q-1))
        board[(r,q)].append((r-1,q+1))
    
    board[(4,-4)].append((3,-4))
    board[(4,-4)].append((4,-3))
    board[(4,-4)].append((3,-3))

    board[(4,-3)].append((4,-4))
    board[(4,-3)].append((4,-2))
    board[(4,-3)].append((3,-3))
    board[(4,-3)].append((3,-2))

    board[(4,-2)].append((4,-3))
    board[(4,-2)].append((4,-2))
    board[(4,-2)].append((3,-2))
    board[(4,-2)].append((3,-1))

    board[(4,-1)].append((4,-2))
    board[(4,-1)].append((4,0))
    board[(4,-1)].append((3,-1))
    board[(4,-1)].append((3,0))

    board[(4,0)].append((4,-1))
    board[(4,0)].append((3,0))
    board[(4,0)].append((3,1))


    board[(3,-4)].append((4,-4))
    board[(3,-4)].append((3,-3))
    board[(3,-4)].append((2,-4))
    board[(3,-4)].append((2,-3))

    board[(2,-4)].append((3,-4))
    board[(2,-4)].append((2,-3))
    board[(2,-4)].append((1,-4))
    board[(2,-4)].append((1,-3))

    board[(1,-4)].append((2,-4))
    board[(1,-4)].append((1,-3))
    board[(1,-4)].append((0,-4))
    board[(1,-4)].append((0,-3))

    board[(0,-4)].append((1,-4))
    board[(0,-4)].append((0,-3))
    board[(0,-4)].append((-1,-3))

    board[(-1,-3)].append((0,-4))
    board[(-1,-3)].append((0,-3))
    board[(-1,-3)].append((-1,-2))
    board[(-1,-3)].append((-2,-2))

    board[(-2,-2)].append((-1,-3))
    board[(-2,-2)].append((-1,-2))
    board[(-2,-2)].append((-2,-1))
    board[(-2,-2)].append((-3,-1))

    board[(-3,-1)].append((-2,-2))
    board[(-3,-1)].append((-2,-1))
    board[(-3,-1)].append((-3,0))
    board[(-3,-1)].append((-4,0))

    board[(-4,0)].append((-3,-1))
    board[(-4,0)].append((-3,0))
    board[(-4,0)].append((-4,1))

    board[(-4,1)].append((-4,0))
    board[(-4,1)].append((-4,2))
    board[(-4,1)].append((-3,0))
    board[(-4,1)].append((-3,1))

    board[(-4,2)].append((-4,1))
    board[(-4,2)].append((-4,3))
    board[(-4,2)].append((-3,1))
    board[(-4,2)].append((-3,2))

    board[(-4,3)].append((-4,2))
    board[(-4,3)].append((-4,4))
    board[(-4,3)].append((-3,2))
    board[(-4,3)].append((-3,3))

    board[(-4,4)].append((-4,3))
    board[(-4,4)].append((-3,3))
    board[(-4,4)].append((-3,4))

    board[(-3,4)].append((-4,4))
    board[(-3,4)].append((-3,3))
    board[(-3,4)].append((-2,3))
    board[(-3,4)].append((-2,4))

    board[(-2,4)].append((-3,4))
    board[(-2,4)].append((-2,3))
    board[(-2,4)].append((-1,3))
    board[(-2,4)].append((-1,4))

    board[(-1,4)].append((-2,4))
    board[(-1,4)].append((-1,3))
    board[(-1,4)].append((0,3))
    board[(-1,4)].append((0,4))

    board[(0,4)].append((-1,4))
    board[(0,4)].append((0,3))
    board[(0,4)].append((1,3))
    
    board[(1,3)].append((0,4))
    board[(1,3)].append((0,3))
    board[(1,3)].append((1,2))
    board[(1,3)].append((2,2))

    board[(2,2)].append((1,3))
    board[(2,2)].append((1,2))
    board[(2,2)].append((2,1))
    board[(2,2)].append((3,1))

    board[(3,1)].append((2,2))
    board[(3,1)].append((2,1))
    board[(3,1)].append((3,0))
    board[(3,1)].append((4,0))

    return board