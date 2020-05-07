# -*- coding: utf-8 -*-
"""
@author: xabi.palmer@gmail.com

"""


from sudoku_class import SudokuClass

quizz= [[0,0,1,7,0,0,6,0,0],
        [7,0,9,0,1,0,3,0,5],
        [6,0,0,0,0,0,0,0,7],
        [0,0,3,0,9,0,4,0,0],
        [0,0,0,8,0,4,0,0,0],
        [0,1,2,0,6,0,5,9,0],
        [9,0,0,0,0,0,0,0,4],
        [1,0,6,0,8,0,9,0,3],
        [0,0,8,6,0,0,7,0,0]]
        
SudokuClass().solve(quizz,show=True)
