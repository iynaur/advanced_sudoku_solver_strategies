# -*- coding: utf-8 -*-
"""
@author: xabi.palmer@gmail.com

"""

import numpy as np
from sudoku_class import SudokuClass
import time


def load_samples(file, count: int):
    
    quizzes = np.zeros((count, 81), np.int32)
    solutions = np.zeros((count, 81), np.int32)
    
    for i, line in enumerate(open(file, 'r').read().splitlines()[1:count]):
        
        quiz, solution = line.replace('.','0').split(",")[:2]        
    
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s

    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    
    return [quizzes, solutions]

#------------------------------------------------------


#Create the solver object
sudoku=SudokuClass()

#Load a set of sudokus from file data test
samples   = load_samples('expert.csv',5000)
quizzs    = samples[0]
solutions = samples[1]
solved    = 0

start_time = time.time()

#For every quizz, try to solve
for i,quizz in enumerate(quizzs):
    print(f'Solving nº {i+1}')
    
    #Compare the correct solution with the returned solution 
    if np.array_equal( sudoku.solve(quizz) , solutions[i] ): 
        solved += 1
    
if solved:  
    sec = round(time.time()-start_time)
    print(f'\nFINISHED: Solved {solved} of {i+1} sudokus in {sec} seconds')
else:
    print('To hard for me!')

# sudoku.tech.show()