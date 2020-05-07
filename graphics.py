# -*- coding: utf-8 -*-
"""
Inspired by 

http://trevorappleton.blogspot.com/2013/10/guide-to-creating-sudoku-solver-using.html

"""

import pygame
from pygame.locals import QUIT

    
def show_board( cells,candidates):
    
    # Sets size of grid
    WINDOWMULTIPLIER = 4 # Modify this number to change size of grid
    WINDOWSIZE = 81
    WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
    WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
    SQUARESIZE = int(WINDOWWIDTH / 3) # size of a 3x3 square
    CELLSIZE = int(SQUARESIZE / 3) # Size of a cell
    NUMBERSIZE = CELLSIZE /3 # Position of unsolved number
    
    # Set up the coloursf
    BLACK     = (0,  0,  0)
    WHITE     = (255,255,255)
    LIGHTGRAY = (200, 200, 200)   
    
    pygame.init()

    ESCALA  = 0.8
    FONTVAL = pygame.font.Font('freesansbold.ttf', int(CELLSIZE*ESCALA))
    FONTBIT = pygame.font.Font('freesansbold.ttf', int(CELLSIZE/3))
    
    dx=CELLSIZE*40/100*ESCALA
    dy=CELLSIZE*20/100*ESCALA

    board = pygame.display.set_mode((WINDOWWIDTH+CELLSIZE,WINDOWHEIGHT+CELLSIZE))
    pygame.display.set_caption('Sudoku Board')
    
    board.fill(WHITE)
   
    #Display values
    for row,tupla in enumerate(cells):
        for col,cell in enumerate(tupla):
                                    
            if cell:
                posx=(col+1)*CELLSIZE+dx
                posy=(row+1)*CELLSIZE+dy
                cellSurf = FONTVAL.render('%s' %(cell), True, BLACK)
                cellRect = cellSurf.get_rect()
                cellRect.topleft = (posx, posy)
                board.blit(cellSurf, cellRect)
                
    #Display possibles
    for row,tupla in enumerate( candidates):
        for col,candidate in enumerate(tupla):

                for number in range(9):
                    
                    if candidate[number]==1:
                        xFactor = (number%3)
                        yFactor=number//3
                        posx=((col+1)*CELLSIZE)+(xFactor*NUMBERSIZE)+dx/3
                        posy=((row+1)*CELLSIZE)+(yFactor*NUMBERSIZE)+dy/3
                        cellSurf = FONTBIT.render('%s' %(number+1), True, BLACK)
                        cellRect = cellSurf.get_rect()
                        cellRect.topleft = (posx, posy)
                        board.blit(cellSurf, cellRect)
                
    for n in range(1,10):
        cellSurf = FONTVAL.render('%s' %(n), True, LIGHTGRAY)
        posx=(CELLSIZE*n)+dx
        posy=dy
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (posx, posy)
        board.blit(cellSurf, cellRect)    
        posy=(CELLSIZE*n)+dy
        posx=dx
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (posx, posy)
        board.blit(cellSurf, cellRect)    

    ### Draw Minor Lines
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(board, LIGHTGRAY, (x+CELLSIZE,CELLSIZE),(x+CELLSIZE,WINDOWHEIGHT+CELLSIZE))
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(board, LIGHTGRAY, (CELLSIZE,y+CELLSIZE), (WINDOWWIDTH+CELLSIZE, y+CELLSIZE))
    
    ### Draw Major Lines
    for x in range(0, WINDOWWIDTH+CELLSIZE, SQUARESIZE): # draw vertical lines
        pygame.draw.line(board, BLACK, (x+CELLSIZE,CELLSIZE),(x+CELLSIZE,WINDOWHEIGHT+CELLSIZE),2)
    for y in range (0, WINDOWHEIGHT+CELLSIZE, SQUARESIZE): # draw horizontal lines
        pygame.draw.line(board, BLACK, (CELLSIZE,y+CELLSIZE), (WINDOWWIDTH+CELLSIZE, y+CELLSIZE),2)

    exiting=False
    while not exiting: #main game loop
    
        pygame.display.update()
        
        for event in pygame.event.get():
            
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                exiting=True
                break
                