"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from collections import defaultdict

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing

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

    board_dict = defaultdict([])
    for category in data:
        for token in data[category]:
            if token:
                if category == "upper":
                    board_dict[(token[1], token[2])].append( "(" + token[0].upper()   + ")" )
                else:
                    board_dict[(token[1], token[2])].append( "(" + token[0] + ")" )
    
    finished = False

    while not finished:
        finished = True
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        for value in board_dict.values():
            if value.isupper():
                finished = False

    
    print_board(board_dict, compact=False)