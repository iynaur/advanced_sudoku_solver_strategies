"""

@author: xabi.palmer@gmail.com

"""
import random
import numpy as np

from cell_class import CellClass
from tupla_class import TuplaClass
from techniques import ALL_TECH
from graphics import show_board


class SudokuClass():

    """
    The sudoku_solver class is an object thar represent the sudoku structure of data as:

        81 cells that can be accesed by a flat array [0..80] or from
        T_rows, T_cols and T_areas that represents each one an array of 9 tuples


    """

    #------------------
    def __init__(self):
    #------------------
        
        self.changed = False

        # Create all cells
        self.cells = np.zeros([9, 9], dtype=CellClass)

        for row, col in np.ndindex(9, 9):
            self.cells[row, col] = CellClass(self, row, 
                                                   col, 
                                                   row//3*3 + col//3) 

        # Create 3 arrays of tuples: areas, rows and columns
        self.t_rows = np.array([TuplaClass(cells) for cells in self.cells])
        self.t_cols = np.array([TuplaClass(cells) for cells in list(self.cells.T)])
        self.t_areas = np.array([TuplaClass(cells) for cells in [
            self.cells[x:x+3, y:y+3].flatten() 
                for x in [0, 3, 6] for y in [0, 3, 6]]])

        # Create a flatten view with all cells
        self.all_cells = self.cells.flatten()


        # Each cell are associates with 3 tuples (row, column and area)
        # and have 20 neighbors
        for cell in self.all_cells:

            cell.t_row = self.t_rows[cell.row_index]
            cell.t_col = self.t_cols[cell.col_index]
            cell.t_area = self.t_areas[cell.area_index]

            cell.neighbors = set(np.concatenate((cell.t_row.cells,
                                                 cell.t_col.cells,
                                                 cell.t_area.cells))) - {cell}
        

    #----------------------------------
    def solve(self, grid, show=False):
    #----------------------------------

        # Check data
        if np.array(grid).shape != (9, 9):
            raise Exception('Bad estructure of data')

        # Reset cells values to a initial state
        for cell in self.all_cells:
            cell.value = 0     
            cell.a_candidates = np.ones(9) 
       

        # Load initial values provided
        for row, col in zip(*np.nonzero(grid)):
            value = int(grid[row][col])
            if value in set(range(1,10)):
                self.cells[row, col].set_value(value)


        # While have wholes and changes, execute every technique in random secuence
        while True:

            # Reset changed flag
            self.changed = False

            # Call every technique in random secuence.
            random.shuffle(ALL_TECH)
            for technique in ALL_TECH:
                technique(self)
                
            # Check if have empty cells
            have_empty_cells = False
            for cell in self.all_cells:
                if cell.value == 0:            
                    have_empty_cells = True
                    break

            # If no more changes and wholes, quit
            if not (have_empty_cells and self.changed):
                break



        # Generate the solution grid
        grid = np.zeros([9, 9], dtype=int)
        
        for cell in self.all_cells:
            grid[cell.row_index, cell.col_index] = cell.value

        if show:
            candidates = [[c.a_candidates for c in tupla.cells] for tupla in self.t_rows]
            show_board(grid, candidates)

        return grid
