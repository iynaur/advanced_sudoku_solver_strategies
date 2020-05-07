# -*- coding: utf-8 -*-
"""
@author: xabi.palmer@gmail.com

"""
from itertools import combinations
import numpy as np


#--------------------------------
def only_in_region(array, value):
#--------------------------------

    # |X|X|X| | | | | | | -> 0
    # | | | |X|X|X| | | | -> 1
    # | | | | | | |X|X|X| -> 2
    # else -> None

    # return 0 if value only can set in any of the first 3 cells in array[0..8] of cells
    # return 1 if value only in the midle 3 cells
    # return 2 if value only in last 3 cells
    # else return None

    in_region=[False, False, False]
    
    for i,cell in enumerate(array):
        in_region[i//3] |= cell.is_candidate(value)

    occupied_regions = np.where(in_region)[0]

    if len(occupied_regions) == 1:
        return occupied_regions[0]  
    return None



#---------------------------------------------
def changes_in_reduced_matrix(original_matrix):
#--------------------
#---------------------------------------------

    matrix = np.array(original_matrix.copy())


    # This process repeats 2 times, 1 for the provide matrix and the other with
    # the transposed version. 
    for cicles in range(2):

        # get rows with 2 or more values possibles
        candidates = set(np.where(np.sum(matrix, axis=1) >= 2)[0])

        # if in the process, a row can only take 1 single candidate,
        # this candidate will be excluded for the rest of the process
        exclusions = set()

        # Create combinatios of 'n' size with all candidates
        for size in range(2, len(candidates)-1):
            for comb in list(combinations(candidates, size)):

                #exclude combinations that have candidates excluded
                combination = set(comb)
                if combination-exclusions != combination:
                    continue

                # check if this combinations have 'size' possibles values
                values_in_comb = np.max(np.take(matrix, comb, 0).T, 1)

                if np.count_nonzero(values_in_comb) == size:

                    # Discard those values from the candidates that not in comb
                    possition_to_remove = np.where(values_in_comb == 1)[0]

                    for candidate in candidates-combination:

                        # Remove candidates
                        matrix[candidate][possition_to_remove] = 0

                        # If only have 1 value, exclude column values and add to exclude list
                        if np.sum(matrix[candidate]) == 1:

                            exclusions.add(candidate)
                            col = list(matrix[candidate]).index(1)
                            matrix[:, col] = 0
                            matrix[candidate][col] = 1

        # Transpose the matriz for the next cicle
        matrix = matrix.T


    #Find diferences
    are_different = original_matrix != matrix
    changed = np.where(are_different)

    # return changes if any
    if len(changed[0]) != 0:
        return list(zip(*changed))
    return []



#------------------------------------
def FIND_UNIQUE_VALUES(sudoku_class):
#------------------------------------

    for tupla in np.concatenate((sudoku_class.t_rows, sudoku_class.t_cols)):

        # If the matrix of candidates have 1 row or column with only 1 value,
        # assign it
    
        matrix = tupla.a_candidates()
        uniques = set() # relation on (index,value) where are uniques values
    
        # Find uniques values in horizontal
        numvalues = np.sum(matrix, 1)
        uniques.update([(i, list(matrix[i]).index(1)+1) for i in np.where(numvalues == 1)[0]])
    
        # Find uniques values in vertical
        matrix = matrix.T
    
        numvalues = np.sum(matrix, 1)
        uniques.update([(list(matrix[i]).index(1), i+1) for i in np.where(numvalues == 1)[0]])
    
        # process the uniques values
        for (index, value) in uniques:
            tupla.cells[index].set_value(value)



#----------------------------------------------------
def REDUCTION_OF_TUPLA_POSSITION_MATRIX(sudoku_class):
#----------------------------------------------------

    # While there's tuplas with recent changes
    for tupla in list(sudoku_class.t_rows) + \
                 list(sudoku_class.t_cols) + \
                 list(sudoku_class.t_areas):

        # If there's changes, apply
        for index, value in changes_in_reduced_matrix(tupla.a_candidates()):
            tupla.cells[index].remove_candidate(value+1)




#----------------------------------------------
def REDUCE_GLOBAL_POSITION_MATRIX(sudoku_class):
#----------------------------------------------

    for value in {1, 2, 3, 4, 5, 6, 7, 8, 9}:

        # Create the possition matrix of each value
        matrix = [[1 if sudoku_class.cells[row, col].is_candidate(value) else 0
                   for col in range(9)] for row in range(9)]

        for row, col in changes_in_reduced_matrix(matrix):
            sudoku_class.cells[row, col].remove_candidate(value)


#--------------------------------------------
def REDUCTION_OF_ASSOCIATED_AREAS(sudoku_class):
#--------------------------------------------

    # If in a row or column, one candidate only can be in 1 región (X),
    # the area that intersec with this 3 cells cant take this
    # candidate in the others cells (Y)

    #  | | | |X|X|X| | | |
    #        |Y|Y|Y|
    #        |Y|Y|Y|


    # For every missing value in every row an col
    for tupla in np.concatenate((sudoku_class.t_rows, sudoku_class.t_cols)):

        for value in tupla.missing():

            # If this value only can be placed in 1 region
            region = only_in_region(tupla.cells, value)
            if region == None:
                continue

            # Remove this candidate from the rest of cells in his area
            for cell in set(tupla.cells[region*3].t_area.cells) - set(tupla.cells):
                if cell.is_candidate(value):
                    cell.remove_candidate(value)


#---------------------------------------------------
def REDUCTION_OF_ASSOCIATED_AREAS_INVERSE(sudoku_class):
#---------------------------------------------------

    # when a value can only be placed in one region (top, mid, bottom) of an area (X)
    # the row than itersec with this region must remove this candidate in
    # the cells than not intersec with this area (Y)

    #  |Y|Y|Y|X|X|X|Y|Y|Y|
    #        | | | |
    #        | | | |


    for cicle in range(2):

        for area in sudoku_class.t_areas:

            # Get the cells of a area (transpose area if cicle ==1)
            cells = area.cells if cicle == 0 else area.as_square().T.flatten()

            #for every missing value,
            for value in area.missing():

                # Check if this value are in onlye 1 region
                region = only_in_region(cells, value)
                if region == None:
                    continue

                #get the tupla that cross with the area along this 3 cells
                pivot = cells[region*3]
                tupla = [pivot.t_row, pivot.t_col][cicle]

                # remove the value in other cells than the common with the area
                for cell in set(tupla.cells) - set(cells):
                    if cell.is_candidate(value):
                        cell.remove_candidate(value)


#-----------------------------------
def OVERLAPPING_SCOPE(sudoku_class):
#-----------------------------------


    def get_scope(cell, value, chain):

        bit = [256, 128, 64, 32, 16, 8, 4, 2, 1][value-1]
        matrix = np.zeros([9, 9], dtype=int)

        for neighbor in cell.neighbors:

            if neighbor.is_candidate(value):
                matrix[neighbor.row_index, neighbor.col_index] = bit

            link = (neighbor, value)
            if not link in chain:

                # if te neighbor is a linked couple
                candidates = neighbor.v_candidates()
                if len(candidates) == 2 and (value in candidates):

                    # Trace scope from this
                    pairvalue = list(candidates - {value})[0]
                    chain.add(link)
                    matrix = np.bitwise_or(matrix, get_scope(neighbor, pairvalue, chain))

        return matrix



    # Get all cells with 2 o more candidates
    num_candidates = np.array([np.sum(c.a_candidates) for c in sudoku_class.all_cells])


    for cell in np.take(sudoku_class.all_cells, np.where(num_candidates >= 2)[0]):

        # Create the intersec scope of every candidate
        for i, value in enumerate(cell.v_candidates()):

            scope_of_v = get_scope(cell, value, set((cell, value)))
            
            if i == 0:
                scope_global = scope_of_v
            else:
                scope_global = np.bitwise_and(scope_global, scope_of_v)


        # If there's common cells, remove the candidates
        for row, col in list(zip(*np.where(scope_global != 0))):

            #convert binary 0b0010 to array [0,0,1,0]
            bits = np.binary_repr(scope_global[row, col], 9)
            state = np.array(list(map(int, list(bits))))

            # process the values
            for value in np.where(state == 1)[0]:
                sudoku_class.cells[row, col].remove_candidate(value+1)





#-----------------------------------------------
def REDUCTION_OF_NEIGBORING_AREAS(sudoku_class):
#-----------------------------------------------

    # in 3 aditional areas, with 3 regions (top, midle a bottom), if a value
    # cant bet assigned in one region in 2 of them areas, the thrird area must
    # have this value in the missing region


    for cicle in range(2):

        if cicle == 0:
            areas = [[sudoku_class.t_areas[row+group].as_square()
                      for group in [0, 1, 2]] for row in [0, 3, 6]]
        else:
            areas = [[sudoku_class.t_areas[row+group].as_square().T
                      for row in [0, 3, 6]] for group in [0, 1, 2]]

        # 3 rows of areas in sudoku
        # every are with 3 groups
        # every group with 3 regions (top, midle, bottom)
        # every region with 3 cells

        # For every value
        for value in {1, 2, 3, 4, 5, 6, 7, 8, 9}:

            # check if the value can be un first, second a third group of the 3 cells
            have = [[[np.array(list(map(lambda e: e.value == value, areas[row][G][R]))).any()
                      for R in [0, 1, 2]] for G in [0, 1, 2]] for row in [0, 1, 2]]

            can = [[[np.array(list(map(lambda e: have[row][G][R] or e.is_candidate(value), areas[row][G][R]))).any()
                     for R in [0, 1, 2]] for G in [0, 1, 2]] for row in [0, 1, 2]]


            for row in [0, 1, 2]:
                for G1, G2, G3 in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
                    for R1, R2, R3 in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
                        if not (have[row][G3][R1] or have[row][G3][R2]):
                            if  not (can[row][G1][R3] or can[row][G2][R3]) or \
                                ((can[row][G1][R1] and not (can[row][G1][R2] or can[row][G1][R3])) and \
                                 (can[row][G2][R2] and not (can[row][G2][R1] or can[row][G2][R3]))):

                                for cell in np.concatenate((areas[row][G3][R1], areas[row][G3][R2])):
                                    if cell.is_candidate(value):
                                        cell.remove_candidate(value)



ALL_TECH = [FIND_UNIQUE_VALUES,
            OVERLAPPING_SCOPE,
            REDUCTION_OF_TUPLA_POSSITION_MATRIX,
            REDUCTION_OF_ASSOCIATED_AREAS,
            REDUCTION_OF_ASSOCIATED_AREAS_INVERSE,
            REDUCTION_OF_NEIGBORING_AREAS,
            REDUCE_GLOBAL_POSITION_MATRIX]
