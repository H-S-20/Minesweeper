import random
from random import randint
import math
from tkinter import *
from tkinter import messagebox
#from astar import *
from copy import copy, deepcopy
from baseAI import AIBrain


class Cell: #Used to flag cells
    def __init__(self,dim):
        self.grid = [[0] * dim for i in range(dim)]
    def setVisited(self,x,y):
        self.grid[x][y] = 1
    def setMasked(self,x,y):
        self.grid[x][y] = 2
    def setFree(self,x,y):
        self.grid[x][y] = 0

class Clue:
    def __init__(self,dim):
        self.grid = [[0] * dim for i in range(dim)]
    def setClue(self,x,y,val):
        self.grid[x][y] = val
    def getClue(self,x,y):
        return self.grid[x][y]

class Map:
    def __init__(self, dim, numMines):
        self.dim = dim
        self.numMines = numMines
        self.free = 2
        self.mine = 3
        self.grid = [[self.free] * dim for i in range(dim)]
        self.visit = Cell(dim)
        self.clue = Clue(dim)
        mines_placed = 0
        while mines_placed < numMines:
            x = randint(0,dim-1)
            y = randint(0,dim-1)
            if self.grid[x][y] != self.mine:
                mines_placed = mines_placed+1
                self.grid[x][y] = self.mine

        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == self.mine:
                    self.clue.setClue(x,y,9)
                else:
                    self.create_clue(x,y)

        # Print grid
        for i in range(len(self.grid)):
            print(self.grid[i])

        print("")
        # Print grid
        for i in range(len(self.grid)):
            print(self.clue.grid[i])

        self.init_ai = 0
        # GUI variables
        self.root = None
        self.canvas = None
        self.new_map = 0  # 0 if no reset requested, 1 if reset requested
        self.gui_grid = [[None] * dim for i in range(dim)]
        self.gui_text = [[None] * dim for i in range(dim)]
        self.reset_button = None

        self.draw_grid()

    def draw_grid(self):
        self.root = Tk()
        self.root.title("Minesweeper - Part 1")
        self.root.geometry("600x640")
        self.root.configure(background = "blue")
        self.canvas = Canvas(self.root, width = 600, height = 600, bg = "red")
        self.reset_button = Button(self.root, text = "reset", command = self.reset)       #Added button for reset
        self.reset_button.grid(row = 0, column = 0, sticky = E, padx = 10, pady = 5, ipadx = 10)
        self.AI_button = Button(self.root, text = "Basic AI")#, command = self.run_ai)
        self.AI_button.bind("<ButtonPress-1>",self.run_ai)
        self.AI_button.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 5, ipadx = 10)

        x1 = 0
        y1 = 0
        offset = 600/self.dim

        for i in range(self.dim):
            for j in range(self.dim):
                fill = "White"

                self.gui_grid[i][j] = self.canvas.create_rectangle(x1, y1, x1+offset, y1+offset, fill = fill, tags="uncover_but")
                self.gui_text[i][j] = self.canvas.create_text(x1+offset/2, y1+offset/2, text="", font=("Papyrus", 26), fill='Black',tags="uncover_but")
                self.canvas.tag_bind("uncover_but","<Button-1>",self.click_square)
                self.canvas.tag_bind("uncover_but","<Button-3>",self.mark_mine)
                y1 = y1 + offset
            x1 = x1 + offset
            y1 = 0

        self.canvas.grid(row=1, column=0) 
        self.root.mainloop()

    def create_clue(self,x,y):
        near_mines = 0
        if x + 1 < self.dim and self.grid[x + 1][y] == self.mine:  # E
            near_mines = near_mines + 1
        if x + 1 < self.dim and y + 1 < self.dim and self.grid[x + 1][y + 1] == self.mine:  # SE
            near_mines = near_mines + 1
        if y + 1 < self.dim and self.grid[x][y + 1] == self.mine:  # S
            near_mines = near_mines + 1
        if x - 1 >= 0 and y + 1 < self.dim and self.grid[x - 1][y + 1] == self.mine:  # SW
            near_mines = near_mines + 1
        if x - 1 >= 0 and self.grid[x - 1][y] == self.mine:  # W
            near_mines = near_mines + 1
        if x - 1 >= 0 and y - 1 >= 0 and self.grid[x - 1][y - 1] == self.mine:  # NW
            near_mines = near_mines + 1
        if y - 1 >= 0 and self.grid[x][y - 1] == self.mine:  # N
            near_mines = near_mines + 1
        if x + 1 < self.dim and y - 1 >= 0 and self.grid[x + 1][y - 1] == self.mine:  # NE
            near_mines = near_mines + 1
        
        self.clue.setClue(x,y,near_mines)

    def mark_mine(self,*args):
        offset = 600/self.dim
        if self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 0:
            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill="Yellow")
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text="Flag", font=("Papyrus", int(32/math.log(self.dim, 2))), fill='Black')
            self.visit.setMasked(int(args[0].x/offset),int(args[0].y/offset))

        elif self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 2:
            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill="White")
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text="", font=("Papyrus", int(32/math.log(self.dim, 2))), fill='Black')
            self.visit.setFree(int(args[0].x/offset),int(args[0].y/offset))

    def click_square(self,*args):
        offset = 600/self.dim
        mineText = "GG"
        if self.visit.grid[int(args[0].x/offset)][int(args[0].y/offset)] == 0:
            fill = "Green"
            text = "0"
            if self.grid[int(args[0].x/offset)][int(args[0].y/offset)] == self.mine:
                fill = "Red"
                text = mineText
            else:
                text = str(self.clue.getClue(int(args[0].x/offset),int(args[0].y/offset)))

            self.canvas.itemconfig(self.gui_grid[int(args[0].x/offset)][int(args[0].y/offset)], fill=fill)
            self.canvas.itemconfig(self.gui_text[int(args[0].x/offset)][int(args[0].y/offset)], text=text, font=("Papyrus", int((32/(math.log(self.dim, 2))))), fill='Black')
            
            if(text == mineText):
                messagebox.showinfo("Result","You lost!")
                self.reset()
            self.visit.setVisited(int(args[0].x/offset),int(args[0].y/offset))

    def run_ai(self,*args):
        if self.init_ai == 0:
            self.ai = AIBrain(self, self.dim, self.numMines)
            self.init_ai = 1
            self.ai.perform_query()
            return

        self.ai.perform_query()

    def reset(self):
        self.root.destroy()
        Map(self.dim,self.numMines)
        
map = Map(15, 30)