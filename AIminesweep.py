import random
from random import randint
import math
from tkinter import *
from copy import copy, deepcopy
#import minesweeper


class AIbrain:
    def __init__(self, map, dim, numBombs):
        self.dim = dim
        self.map = map
        self.numBombs = numBombs
        self.grid_prob = [[((numBombs)/(dim**2))] * dim for i in range(dim)]
        self.grid_mem = [[0] * dim for i in range(dim)]
        self.grid_known = [[0] * dim for i in range(dim)]
        #print probability grid
        for i in range(len(self.grid_prob)):
            print(self.grid_prob[i])
        
        print(" ")

        #print memory grid
        for i in range(len(self.grid_mem)):
            print(self.grid_mem[i])

        print(" ")

        for i in range(len(self.grid_known)):
            print(self.grid_known[i])

        #This will be the first index tested at random
        xran = randint(0, dim - 1)
        yran = randint(0, dim - 1)

        offset = 600/dim

        self.checkGrid(xran, yran)

    def checkGrid(self, xval, yval):
        if self.map.visit.grid[xval][yval] == 0:
            fill = "Green"
            text = "0"
            nearMines = 0
            if self.map.grid[xval][yval] == self.map.mine:
                fill = "Red"
                text = "GG"
            else:
                if xval+1 < self.dim and self.map.grid[xval+1][yval] == self.map.mine: #S
                    nearMines = nearMines + 1
                if xval+1 < self.dim and yval+1 < self.dim and self.map.grid[xval+1][yval+1] == self.map.mine: #SE
                    nearMines = nearMines + 1
                if yval+1 < self.dim and self.map.grid[xval][yval+1] == self.map.mine: #E
                    nearMines = nearMines + 1
                if xval-1 >= 0 and yval+1 < self.dim and self.map.grid[xval-1][yval+1] == self.map.mine: #NE
                    nearMines = nearMines + 1
                if xval-1 >= 0 and self.map.grid[xval-1][yval] == self.map.mine: #N
                    nearMines = nearMines + 1
                if xval-1 >= 0 and yval-1 >= 0 and self.map.grid[xval-1][yval-1] == self.map.mine: #NW
                    nearMines = nearMines + 1
                if yval-1 >= 0 and self.map.grid[xval][yval-1] == self.map.mine: #W
                    nearMines = nearMines + 1
                if xval+1 < self.dim and yval-1 >= 0 and self.map.grid[xval+1][yval-1] == self.map.mine: #SW
                    nearMines = nearMines + 1
                
                text = str(nearMines)
            self.map.canvas.itemconfig(self.map.gui_grid[xval][yval], fill=fill)
            self.map.canvas.itemconfig(self.map.gui_text[xval][yval], text=text, font=("Papyrus", 32), fill='Black')
            self.map.visit.setVisited(xval,yval)

#AIbrain(5,5)