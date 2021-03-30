"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import math
import random
from collections import defaultdict
import time

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
        print("usage: python3 -m search path/to/input.json", file = sys.stderr)
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
    elude = defaultdict(list)
    #store uppper token as key and its steps as values
    upper_path = defaultdict(list)
    
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
                    #initialize the upper_path
                    upper_path[(token[1], token[2])] = []
                else:
                    board_dict[(token[1], token[2])].append( "(" + token[0] + ")" )
                    if category == "lower":
                        #board_dict[(token[1], token[2])].append(token[0])
                        lower[(token[1], token[2])].append(token[0])
                    elif category == "block":
                        block.append((token[1], token[2]))

    #assign target to upper token
    for i in upper.keys():
        for j in lower.keys():
            if defeat(upper[i], lower[j]):
                target[i].append(j)
            elif defeat(lower[j], upper[i]):
                elude[i].append(j)

    #while lower can not move, the path just need to be calculated oncely

    while lower:

        for current_upper_token in upper_path.keys():
            
            a_star(current_upper_token, target, upper_path, board, block, upper)

            path = upper_path[current_upper_token]
            origin = path[-1]
            move_to = path[-2]

            upper[move_to] = upper[origin]
            del upper[origin]

            '''
            #remove current target from lower dict
            del lower[tar]

            # we only care about the first step of the moves
            move_to = path[-1]
            
            # TODO: game rule check if the block we move into conatin any defeats

            board_dict[move_to] = board_dict[i]
            board_dict.pop(i)

            upper[move_to] = upper[i]
            upper.pop(i)
            '''
            
            #check whether swing or slide
            if distance(origin, move_to) > 1:
                print_swing(turn, origin[0], origin[1], move_to[0], move_to[1])
            else:
                print_slide(turn, origin[0], origin[1], move_to[0], move_to[1])
            
            #remove strating hex from path
            path.remove(origin)
            
            #empty the path's list and kill the target when path finishes
            if len(path) == 1:
            
                #remove the be killed target from target list
                for i in target:
                    if path[-1] in target[i]:
                        target[i].remove(path[-1])

                del lower[path[-1]]
                del path[-1]

        turn += 1
        #time.sleep(2)


def a_star(original_upper_token, target, upper_path, board, block, upper):

    if upper_path[original_upper_token]:
        current_upper_token = upper_path[original_upper_token][-1]
    else:
        current_upper_token = original_upper_token
    

    frontier = PriorityQueue()

    tar = target[original_upper_token][0]
            
    if target[original_upper_token]:
        tar = target[original_upper_token][0]
    else:
        tar = board[original_upper_token][random.randint(0, len(target[original_upper_token])-1)]
            
    frontier.put((0, current_upper_token))
    cost_dict = {}
    path = []
    come_from = {}
    cost_dict[current_upper_token] = 0

    while not frontier.empty():
        current = frontier.get()[1]
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
            if neighbour not in cost_dict.keys() or cost < cost_dict[neighbour]:
                cost_dict[neighbour] = cost
                come_from[neighbour] = current
                frontier.put((cost + distance(tar, neighbour), neighbour))

    # get the path from target back to start
    # path tracking implementation inspired by https://www.redblobgames.com/pathfinding/a-star/implementation.html
    path.append(tar)
    while come_from[tar] != current_upper_token:
        path.append(come_from[tar])
        tar = come_from[tar]
    path.append(come_from[tar])

    #add path to corresponding upper token
    upper_path[original_upper_token] = path
    print(path)

def distance(first, second):
    return (abs(first[1] - second[1]) + abs(first[1] - second[1] + first[0] - second[0]) + abs(first[0] - second[0])) / 2

def defeat(first, second):
    f = first[0].lower()
    s = second[0].lower()

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