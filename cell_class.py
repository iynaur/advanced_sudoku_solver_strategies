# -*- coding: utf-8 -*-
"""
@author: xabi.palmer@gmail.com

"""

import numpy as np

class CellClass():


    #------------------------------------------------------------
    def __init__(self, parent, row_index, col_index, area_index):
    #------------------------------------------------------------

        self.parent = parent
        
        # Initially, no value and all 9 candidates are possibles ("1")
        self.value = 0
        self.a_candidates = np.ones(9)

        # Get row, column and area number 
        self.row_index = row_index   # 0..8
        self.col_index = col_index   # 0..8
        self.area_index = area_index  # 0..8
        self.pos_in_t_area = row_index%3*3 + col_index%3  # [0..8]
        
        # Declare the 3 tuples that every cell are associated to
        self.t_row = None
        self.t_col = None
        self.t_area = None
        
        # Declare the set for indentify the neigbors of each cell
        self.neighbors = set()
        
        

    #------------------------------
    def set_value(self, new_value):
    #------------------------------

        # Ignore if is the current value
        if self.value == new_value:
            return

        # check integrity
        if self.value != 0:
            raise Exception('Cant assign 2 values')

        if not self.is_candidate(new_value):
            raise Exception('Cant assign a value not in candidates')

        # Assign value and discard all candidates
        self.value = new_value
        self.a_candidates = np.zeros(9)

        # Remove value from candidates in neighbors
        for cell in self.neighbors:
            if cell.is_candidate(new_value):
                cell.remove_candidate(new_value)

        # notify to the sudoku that has changed
        self.parent.changed = True


    #-----------------------------
    def is_candidate(self, value): 
    #-----------------------------
        """
        determine si a certain value is a candidate to the empty cell
        """

        return self.a_candidates[value-1] == 1 


    #---------------------------------
    def remove_candidate(self, value):
    #---------------------------------
        """
        remove a certaint value from the candidates list
        """

        if not self.is_candidate(value):
            raise Exception(f'Candidate {value} not found')

        self.a_candidates[value-1] = 0   
        self.parent.changed = True


    #----------------------
    def v_candidates(self):
    #----------------------
        """
        return the list of candidates values
        if a_candidates=[0,1,0,0,0,1,0,1,0] returns (2,6,8)
        """
        return set(np.add(np.where(self.a_candidates == 1)[0], 1))
