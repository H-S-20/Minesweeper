from random import randint
from tkinter import *
import math

class AICell:
    def __init__(self, x, y, status, dim, map, ai_cells):
        self.x = x
        self.y = y
        self.status = status  # 1 clicked(uncovered), 2 = covered, 3 = flagged, 4=exploded
        self.dim = dim
        self.map = map
        self.ai_cells = ai_cells
        self.near_mines = self.map.clue.getClue(x,y)  # the clue
        self.safe_neighbors = []
        self.identified_mines = []
        self.hidden_neighbors = []

    def update_all(self): #Updates three lists based on the given cell's surroundings
        self.safe_neighbors.clear() #List to identify uncovered adjacent boxes -- denoted as 1
        self.hidden_neighbors.clear() #List to identify covered adjacent boxes -- denoted as 2
        self.identified_mines.clear() #List to identify known adjacent mines -- denoted as 3
        if self.x + 1 < self.dim:
            #EAST
            if self.ai_cells[self.x + 1][self.y].status == 1:
                self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y])
            elif self.ai_cells[self.x + 1][self.y].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y])
            else:
                self.identified_mines.append(self.ai_cells[self.x + 1][self.y])

            #SOUTHEAST
            if self.y + 1 < self.dim:
                if self.ai_cells[self.x + 1][self.y + 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y+1])
                elif self.ai_cells[self.x + 1][self.y + 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y+1])
                else:
                    self.identified_mines.append(self.ai_cells[self.x + 1][self.y+1])

            #NORTHEAST
            if self.y - 1 >= 0:
                if self.ai_cells[self.x + 1][self.y - 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y-1])
                elif self.ai_cells[self.x + 1][self.y - 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y-1])
                else:
                    self.identified_mines.append(self.ai_cells[self.x + 1][self.y-1])

        if self.x - 1 >= 0:
            #WEST
            if self.ai_cells[self.x-1][self.y].status == 1:
                self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y])
            elif self.ai_cells[self.x-1][self.y].status == 2: 
                self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y])
            else:
                self.identified_mines.append(self.ai_cells[self.x - 1][self.y])

            #SOUTHWEST
            if self.y + 1 < self.dim:
                if self.ai_cells[self.x - 1][self.y + 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y+1])
                elif self.ai_cells[self.x - 1][self.y + 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y+1])
                else:
                    self.identified_mines.append(self.ai_cells[self.x - 1][self.y+1])

            #NORTHWEST
            if self.y - 1 < self.dim:
                if self.ai_cells[self.x - 1][self.y - 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y-1])
                elif self.ai_cells[self.x - 1][self.y - 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y-1])
                else:
                    self.identified_mines.append(self.ai_cells[self.x - 1][self.y-1])

        #SOUTH
        if self.y + 1 < self.dim:
            if self.ai_cells[self.x][self.y + 1].status == 1:  # E
                self.safe_neighbors.append(self.ai_cells[self.x][self.y + 1])
            elif self.ai_cells[self.x][self.y + 1].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x][self.y+1])
            else:
                self.identified_mines.append(self.ai_cells[self.x][self.y+1])

        #NORTH
        if self.y - 1 < self.dim:
            if self.ai_cells[self.x][self.y - 1].status == 1:  # E
                self.safe_neighbors.append(self.ai_cells[self.x][self.y - 1])
            elif self.ai_cells[self.x][self.y - 1].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x][self.y-1])
            else:
                self.identified_mines.append(self.ai_cells[self.x][self.y-1])

    def count_neighbors(self): #Used for safety detection
        count = 0
        if self.x + 1 < self.dim:
            count = count + 1
        if self.x + 1 < self.dim and self.y + 1 < self.dim:
            count = count + 1
        if self.y + 1 < self.dim:
            count = count + 1
        if self.x > 0 and self.y + 1 < self.dim:
            count = count + 1
        if self.x > 0:
            count = count + 1
        if self.x > 0 and self.y > 0:
            count = count + 1
        if self.y > 0:
            count = count + 1
        if self.x + 1 < self.dim and self.y > 0:
            count = count + 1
        return count


class AIBrain:
    def __init__(self, map, dim, num_mines):
        self.dim = dim
        self.map = map
        self.num_mines = num_mines
        self.ai_cells = [[0] * dim for i in range(dim)]
        self.init_ai_cells()
        self.moves = []

    def init_ai_cells(self):
        for x in range(self.dim):
            for y in range(self.dim):
                self.ai_cells[x][y] = AICell(x, y, 2, self.dim, self.map, None) #Get clue value, initialize lists for neighbor knowns/unknowns
        for x in range(self.dim): 
            for y in range(self.dim):
                self.ai_cells[x][y].ai_cells = self.ai_cells

    def check_grid(self, xval, yval):
        if self.map.visit.grid[xval][yval] == 0:
            fill = "Green"
            text = str(self.map.clue.getClue(xval,yval))

            if self.map.grid[xval][yval] == self.map.mine:
                fill = "Red"
                text = "GG"

            if self.ai_cells[xval][yval].status == 3:
                fill = "salmon"
                text = "Flag"

            self.map.canvas.itemconfig(self.map.gui_grid[xval][yval], fill=fill)
            self.map.canvas.itemconfig(self.map.gui_text[xval][yval], text=text, font=("Papyrus", int(32/math.log(self.dim, 2))), fill='Black')

            if fill == "Green":
                self.ai_cells[xval][yval].status = 1 #Set to uncovered
                self.map.visit.setVisited(xval, yval) #Update map
            
            if fill == "Red":
                self.ai_cells[xval][yval].status = 4 #Set to exploded
                self.map.visit.setVisited(xval, yval) #Update map

    def update_all_cells(self):
        for x in range(len(self.ai_cells)):
            for y in range(len(self.ai_cells[0])):
                if self.ai_cells[x][y].status == 1:
                    self.ai_cells[x][y].update_all()

    def assess_knowledge(self):
        self.update_all_cells()
        for x in range(len(self.ai_cells)):
            for y in range(len(self.ai_cells[0])):
                temp_cell = self.ai_cells[x][y]
                if temp_cell.status == 1: #If cell is uncovered
                    if temp_cell.near_mines - len(temp_cell.identified_mines) == len(temp_cell.hidden_neighbors):
                    #if clue - known adjacent mines = covered squares left
                        # Every hidden neighbor is a mine
                        for i in range(len(temp_cell.hidden_neighbors)):
                            temp_cell.hidden_neighbors[i].status = 3
                            self.moves.append((temp_cell.hidden_neighbors[i].x, temp_cell.hidden_neighbors[i].y))

                    self.update_all_cells()
                    #print("("+repr(x)+", "+repr(y)+") "+repr(temp_cell.count_neighbors())+" "+repr(temp_cell.near_mines)+" "+repr(len(temp_cell.safe_neighbors))+" "+repr(len(temp_cell.hidden_neighbors)))
                    if (temp_cell.count_neighbors() - temp_cell.near_mines) - len(temp_cell.safe_neighbors) == len(temp_cell.hidden_neighbors):
                    #if (all adjacents - clue) - all uncovered adjacents = covered squares left
                        # Every hidden neighbor is safe
                        for i in range(len(temp_cell.hidden_neighbors)):
                            temp_cell.hidden_neighbors[i].status = 1
                            self.moves.append((temp_cell.hidden_neighbors[i].x, temp_cell.hidden_neighbors[i].y))
    
    def perform_query(self):
        self.assess_knowledge()
        if len(self.moves) == 0: # After assessing all knowns, no hidden cell can be marked as a mine or safe
            covered = []
            for i in range(len(self.ai_cells)): #Generate list of all unknown cells
                for j in range(len(self.ai_cells[0])):
                    if self.ai_cells[i][j].status == 2:
                        covered.append(self.ai_cells[i][j])

            # Choose randomly from covered cells
            if len(covered) > 0:
                rand_idx = randint(0, len(covered) - 1)
                rand_cell = covered[rand_idx]
                self.check_grid(rand_cell.x, rand_cell.y)
                print("Testing random cell: " + str(rand_cell.x) + " " + str(rand_cell.y))
        else:
            print("Moves:", end="")
            print(self.moves)
            for (i, j) in self.moves:
                self.check_grid(i, j)

            self.moves.clear()
            #self.print_grids()

    # Used for debugging
    def print_grids(self):
        print("AI GRID")
        for i in range(len(self.ai_cells)):
            for j in range(len(self.ai_cells[i])):
                print(self.ai_cells[i][j].status, end=" ")
            print()
        print("AI GRID HIDDEN NEIGHBORS")

        for i in range(len(self.ai_cells)):
            for j in range(len(self.ai_cells[i])):
                self.ai_cells[i][j].update_hidden_neighbors()
                print(len(self.ai_cells[i][j].hidden_neighbors), end=" ")
            print()
        print("MAP GRID")
        for i in range(len(self.map.grid)):
            for j in range(len(self.map.grid[i])):
                print(self.map.grid[i][j], end=" ")
            print()

        print("VISIT GRID")
        for i in range(len(self.map.visit.grid)):
            for j in range(len(self.map.visit.grid[i])):
                print(self.map.visit.grid[i][j], end=" ")
            print()
