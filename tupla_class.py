# -*- coding: utf-8 -*-
"""
@author: xabi.palmer@gmail.com

"""

import numpy as np


class TuplaClass():

    """
    A tupla is a collection of 9 cells

    It has a property "missing" that repressents the list of 1..9 values that are
    missing in his cells
    """

    #---------------------------------------
    def __init__(self, a_cells):
    #---------------------------------------

        self.cells = a_cells 


    #----------------------
    def a_candidates(self):
    #----------------------
        """
        return a list of all candidates of all cells
        """

        return np.array([cell.a_candidates for cell in self.cells])


    #-----------------
    def missing(self):
    #-----------------
        """
        return the list of values that are not assigned to the tupla
        """

        return set(range(1,10)) - set([cell.value for cell in self.cells])


    #-------------------
    def as_square(self):
    #-------------------
        """
        return a 3x3 version of the cells in the tupla
        """
        return np.array([self.cells[n:n+3] for n in [0, 3, 6]])
