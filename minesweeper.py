import random
from random import randint
import math
from tkinter import *
#from astar import *
from copy import copy, deepcopy

class Cell: #Used to flag cells
    def __init__(self,dim):
        self.grid = [[0] * dim for i in range(dim)]
    def setVisited(self,x,y):
        self.grid[x][y] = 1
    def setMasked(self,x,y):
        self.grid[x][y] = 2
    def setFree(self,x,y):
        self.grid[x][y] = 0

class Map:
    def __init__(self, dim, numMines):
        self.dim = dim
        self.free = 2
        self.mine = 3
        self.grid = [[self.free] * dim for i in range(dim)]
        self.visit = Cell(dim)
        mines_placed = 0
        while mines_placed < numMines:
            x = randint(0,dim-1)
            y = randint(0,dim-1)
            if self.grid[x][y] != self.mine:
                mines_placed = mines_placed+1
                self.grid[x][y] = self.mine
        #self.cells = random.choices([0, 1], [1 - probP, probP], k=(dim * dim))
        #self.manipGrid(self.grid, self.cells)
        self.path_tuples = []

        # Print grid
        for i in range(len(self.grid)):
            print(self.grid[i])


        # GUI variables
        self.root = None
        self.canvas = None
        self.a_star_man_button = None
        self.new_map = 0  # 0 if no reset requested, 1 if reset requested
        self.gui_grid = [[None] * dim for i in range(dim)]
        self.gui_text = [[None] * dim for i in range(dim)]

        self.draw_grid()

    

    def manipGrid(self, testGrid, testCells):
        k = 0
        for i in range(len(testGrid)):
            for j in range(len(testGrid[i])):
                testGrid[i][j] = testCells[k]
                k = k + 1
        testGrid[0][0] = 2
        testGrid[len(testGrid) - 1][len(testGrid[i]) - 1] = 3

    def draw_grid(self):
        self.root = Tk()
        self.root.title("MazeRunner - Part 1")
        self.root.geometry("600x600")
        self.root.configure(background = "black")
        self.canvas = Canvas(self.root, width = 600, height = 600, bg = "black")
        #self.a_star_man_button = Button(self.root, text = "AStar Manhattan Search", command = self.a_star_man)
        #self.a_star_man_button.grid(row= 0, column = 0, sticky = W, padx = 320, pady = 10)

        x1 = 0
        y1 = 0
        offset = 600/self.dim

        for i in range(self.dim):
            for j in range(self.dim):
                fill = "White"

                #playbutton = c.create_rectangle(75, 25, 225, 75, fill="red",tags="playbutton")
                #playtext = c.create_text(150, 50, text="Play", font=("Papyrus", 26), fill='blue',tags="playbutton")

                #c.tag_bind("playbutton","<Button-1>",clicked)

                self.gui_grid[i][j] = self.canvas.create_rectangle(x1, y1, x1+offset, y1+offset, fill = fill, tags="uncover_but")
                self.gui_text[i][j] = self.canvas.create_text(x1+offset/2, y1+offset/2, text="", font=("Papyrus", 26), fill='Black')
                #self.canvas.create_text(int(args[0].x/offset)*offset+offset/2, int(args[0].y/offset)*offset+offset/2, text=text, font=("Papyrus", 26), fill='Black')
                self.canvas.tag_bind("uncover_but","<Button-1>",self.click_square)
                self.canvas.tag_bind("uncover_but","<Button-3>",self.mark_mine)
                y1 = y1 + offset
            x1 = x1 + offset
            y1 = 0

        self.canvas.grid(row=1, column=0)
        self.root.mainloop()

    def mark_mine(self,*args):
        offset = 600/self.dim
        #print(self.canvas.itemcget(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)],"state"))
        #print(args)
        if self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 0:
            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill="Yellow")
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text="NO TOUCHY", font=("Papyrus", 10), fill='Black')
            self.visit.setMasked(int(args[0].x/offset),int(args[0].y/offset))

        elif self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 2:
            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill="White")
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text="", font=("Papyrus", 10), fill='Black')
            self.visit.setFree(int(args[0].x/offset),int(args[0].y/offset))

    def click_square(self,*args):
        offset = 600/self.dim
        if self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 0:
            fill = "Green"
            text = "0"
            nearMines = 0
            if self.grid[int(args[0].x/offset)][int(args[0].y/offset)] == self.mine:
                fill = "Red"
                text = "D:"
            else:
                if int(args[0].x/offset)+1 < self.dim and self.grid[int(args[0].x/offset)+1][int(args[0].y/offset)] == self.mine: #S
                    nearMines = nearMines + 1
                if int(args[0].x/offset)+1 < self.dim and int(args[0].y/offset)+1 < self.dim and self.grid[int(args[0].x/offset)+1][int(args[0].y/offset)+1] == self.mine: #SE
                    nearMines = nearMines + 1
                if int(args[0].y/offset)+1 < self.dim and self.grid[int(args[0].x/offset)][int(args[0].y/offset)+1] == self.mine: #E
                    nearMines = nearMines + 1
                if int(args[0].x/offset)-1 >= 0 and int(args[0].y/offset)+1 < self.dim and self.grid[int(args[0].x/offset)-1][int(args[0].y/offset)+1] == self.mine: #NE
                    nearMines = nearMines + 1
                if int(args[0].x/offset)-1 >= 0 and self.grid[int(args[0].x/offset)-1][int(args[0].y/offset)] == self.mine: #N
                    nearMines = nearMines + 1
                if int(args[0].x/offset)-1 >= 0 and int(args[0].y/offset)-1 >= 0 and self.grid[int(args[0].x/offset)-1][int(args[0].y/offset)-1] == self.mine: #NW
                    nearMines = nearMines + 1
                if int(args[0].y/offset)-1 >= 0 and self.grid[int(args[0].x/offset)][int(args[0].y/offset)-1] == self.mine: #W
                    nearMines = nearMines + 1
                if int(args[0].x/offset)+1 < self.dim and int(args[0].y/offset)-1 >= 0 and self.grid[int(args[0].x/offset)+1][int(args[0].y/offset)-1] == self.mine: #SW
                    nearMines = nearMines + 1
                
                text = str(nearMines)
            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill=fill)
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text=text, font=("Papyrus", 32), fill='Black')
            self.visit.setVisited(int(args[0].x/offset),int(args[0].y/offset))

    def draw_path(self):
        for i in range(len(self.gui_grid)):
            for j in range(len(self.gui_grid[i])):
                if (i, j) in self.path_tuples and (i, j) != (0, 0) and (i, j) != (self.dim-1, self.dim-1):
                    self.canvas.itemconfig(self.gui_grid[i][j], fill="Blue")
                if (i,j) not in self.path_tuples and (i, j) != (0, 0) and (i, j) != (self.dim - 1, self.dim - 1) and self.grid[i][j] == 0:
                    self.canvas.itemconfig(self.gui_grid[i][j], fill="White")
map = Map(5, 5)