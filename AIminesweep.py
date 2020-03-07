from random import randint
from tkinter import *
import math

class AICell:
    def __init__(self, x, y, status, dim, map, ai_cells):
        self.x = x
        self.y = y
        self.status = status  # 1 clicked(uncovered), 2 = covered, 3 = mine
        self.dim = dim
        self.map = map
        self.ai_cells = ai_cells
        self.near_mines = 0  # the clue
        self.count_neighbor_mines()
        self.safe_neighbors = []
        self.identified_mines = []
        self.hidden_neighbors = []

        self.deduced_mine = False

    def count_neighbor_mines(self):
        self.near_mines = 0
        if self.x + 1 < self.dim and self.map.grid[self.x + 1][self.y] == self.map.mine:  # S
            self.near_mines = self.near_mines + 1
        if self.x + 1 < self.dim and self.y + 1 < self.dim and self.map.grid[self.x + 1][self.y + 1] == self.map.mine:  # SE
            self.near_mines = self.near_mines + 1
        if self.y + 1 < self.dim and self.map.grid[self.x][self.y + 1] == self.map.mine:  # E
            self.near_mines = self.near_mines + 1
        if self.x - 1 >= 0 and self.y + 1 < self.dim and self.map.grid[self.x - 1][self.y + 1] == self.map.mine:  # NE
            self.near_mines = self.near_mines + 1
        if self.x - 1 >= 0 and self.map.grid[self.x - 1][self.y] == self.map.mine:  # N
            self.near_mines = self.near_mines + 1
        if self.x - 1 >= 0 and self.y - 1 >= 0 and self.map.grid[self.x - 1][self.y - 1] == self.map.mine:  # NW
            self.near_mines = self.near_mines + 1
        if self.y - 1 >= 0 and self.map.grid[self.x][self.y - 1] == self.map.mine:  # W
            self.near_mines = self.near_mines + 1
        if self.x + 1 < self.dim and self.y - 1 >= 0 and self.map.grid[self.x + 1][self.y - 1] == self.map.mine:  # SW
            self.near_mines = self.near_mines + 1

    def update_safe_neighbors(self):
        self.safe_neighbors.clear()
        if self.x + 1 < self.dim and self.ai_cells[self.x + 1][self.y].status == 1:  # S
            self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y])
        if self.x + 1 < self.dim and self.y + 1 < self.dim and self.ai_cells[self.x + 1][self.y + 1].status == 1:  # SE
            self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y + 1])
        if self.y + 1 < self.dim and self.ai_cells[self.x][self.y + 1].status == 1:  # E
            self.safe_neighbors.append(self.ai_cells[self.x][self.y + 1])
        if self.x - 1 >= 0 and self.y + 1 < self.dim and self.ai_cells[self.x - 1][self.y + 1].status == 1:  # NE
            self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y + 1])
        if self.x - 1 >= 0 and self.ai_cells[self.x - 1][self.y].status == 1:  # N
            self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y])
        if self.x - 1 >= 0 and self.y - 1 >= 0 and self.ai_cells[self.x - 1][self.y - 1].status == 1:  # NW
            self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y - 1])
        if self.y - 1 >= 0 and self.ai_cells[self.x][self.y - 1].status == 1:  # W
            self.safe_neighbors.append(self.ai_cells[self.x][self.y - 1])
        if self.x + 1 < self.dim and self.y - 1 >= 0 and self.ai_cells[self.x + 1][self.y - 1].status == 1:  # SW
            self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y - 1])

    def update_identified_mines(self):
        self.identified_mines.clear()
        if self.x + 1 < self.dim and self.ai_cells[self.x + 1][self.y].status == 3:  # S
            self.identified_mines.append(self.ai_cells[self.x + 1][self.y])
        if self.x + 1 < self.dim and self.y + 1 < self.dim and self.ai_cells[self.x + 1][self.y + 1].status == 3:  # SE
            self.identified_mines.append(self.ai_cells[self.x + 1][self.y + 1])
        if self.y + 1 < self.dim and self.ai_cells[self.x][self.y + 1].status == 3:  # E
            self.identified_mines.append(self.ai_cells[self.x][self.y + 1])
        if self.x - 1 >= 0 and self.y + 1 < self.dim and self.ai_cells[self.x - 1][self.y + 1].status == 3:  # NE
            self.identified_mines.append(self.ai_cells[self.x - 1][self.y + 1])
        if self.x - 1 >= 0 and self.ai_cells[self.x - 1][self.y].status == 3:  # N
            self.identified_mines.append(self.ai_cells[self.x - 1][self.y])
        if self.x - 1 >= 0 and self.y - 1 >= 0 and self.ai_cells[self.x - 1][self.y - 1].status == 3:  # NW
            self.identified_mines.append(self.ai_cells[self.x - 1][self.y - 1])
        if self.y - 1 >= 0 and self.ai_cells[self.x][self.y - 1].status == 3:  # W
            self.identified_mines.append(self.ai_cells[self.x][self.y - 1])
        if self.x + 1 < self.dim and self.y - 1 >= 0 and self.ai_cells[self.x + 1][self.y - 1].status == 3:  # SW
            self.identified_mines.append(self.ai_cells[self.x + 1][self.y - 1])

    def update_hidden_neighbors(self):
        self.hidden_neighbors.clear()
        if self.x + 1 < self.dim and self.ai_cells[self.x + 1][self.y].status == 2:  # S
            self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y])
        if self.x + 1 < self.dim and self.y + 1 < self.dim and self.ai_cells[self.x + 1][self.y + 1].status == 2:  # SE
            self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y + 1])
        if self.y + 1 < self.dim and self.ai_cells[self.x][self.y + 1].status == 2:  # E
            self.hidden_neighbors.append(self.ai_cells[self.x][self.y + 1])
        if self.x - 1 >= 0 and self.y + 1 < self.dim and self.ai_cells[self.x - 1][self.y + 1].status == 2:  # NE
            self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y + 1])
        if self.x - 1 >= 0 and self.ai_cells[self.x - 1][self.y].status == 2:  # N
            self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y])
        if self.x - 1 >= 0 and self.y - 1 >= 0 and self.ai_cells[self.x - 1][self.y - 1].status == 2:  # NW
            self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y - 1])
        if self.y - 1 >= 0 and self.ai_cells[self.x][self.y - 1].status == 2:  # W
            self.hidden_neighbors.append(self.ai_cells[self.x][self.y - 1])
        if self.x + 1 < self.dim and self.y - 1 >= 0 and self.ai_cells[self.x + 1][self.y - 1].status == 2:  # SW
            self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y - 1])


class AIBrain:
    def __init__(self, map, dim, num_mines):
        self.dim = dim
        self.map = map
        self.num_mines = num_mines
        self.ai_cells = [[0] * dim for i in range(dim)]
        self.init_ai_cells()
        self.moves = []

    def init_ai_cells(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.ai_cells[i][j] = AICell(i, j, 2, self.dim, self.map, None) #Get clue value
        for i in range(self.dim):
            for j in range(self.dim):
                self.ai_cells[i][j].ai_cells = self.ai_cells

    def check_grid(self, xval, yval):
        if self.map.visit.grid[xval][yval] == 0:
            fill = "Green"
            text = str((self.ai_cells[xval][yval]).near_mines)

            if self.map.grid[xval][yval] == self.map.mine:
                fill = "Red"
                text = "GG"

            if self.ai_cells[xval][yval].deduced_mine:
                fill = "Yellow"
                text = "Flag"

            self.map.canvas.itemconfig(self.map.gui_grid[yval][xval], fill=fill)
            self.map.canvas.itemconfig(self.map.gui_text[yval][xval], text=text, font=("Papyrus", int(32/math.log(self.dim, 2))), fill='Black')

            if fill != "Yellow":
                self.ai_cells[xval][yval].status = 1 #Set to uncovered
                self.map.visit.setVisited(xval, yval) #Update map

    def assess_knowledge(self):
        self.update_all_cells()
        for i in range(len(self.ai_cells)):
            for j in range(len(self.ai_cells[i])):
                temp_cell = self.ai_cells[i][j]
                if temp_cell.status == 2:
                    continue
                if temp_cell.near_mines - len(temp_cell.identified_mines) == len(temp_cell.hidden_neighbors):
                    # every hidden neighbor is a mine
                    for idx in range(len(temp_cell.hidden_neighbors)):
                        temp_cell.hidden_neighbors[idx].status = 3
                        temp_cell.hidden_neighbors[idx].deduced_mine = True
                        self.moves.append((temp_cell.hidden_neighbors[idx].x, temp_cell.hidden_neighbors[idx].y, "mine"))

                self.update_all_cells()
                if (8 - temp_cell.near_mines) - len(temp_cell.safe_neighbors) == len(temp_cell.hidden_neighbors):
                    # every hidden neighbor is safe
                    for idx in range(len(temp_cell.hidden_neighbors)):
                        temp_cell.hidden_neighbors[idx].status = 1
                        self.moves.append((temp_cell.hidden_neighbors[idx].x, temp_cell.hidden_neighbors[idx].y, "safe"))

    def perform_query(self):
        self.assess_knowledge()
        if len(self.moves) == 0:
            # after assessing all known info, no hidden cell can be conclusively identified as a mine or safe
            uncovered = []
            for i in range(len(self.ai_cells)):
                for j in range(len(self.ai_cells[i])):
                    if self.ai_cells[i][j].status == 2:
                        uncovered.append(self.ai_cells[i][j])

            # choose randomly from uncovered cells
            if len(uncovered) > 0:
                rand_idx = randint(0, len(uncovered) - 1)
                rand_cell = uncovered[rand_idx]
                self.check_grid(rand_cell.x, rand_cell.y)
                print("Testing random cell: " + str(rand_cell.x) + " " + str(rand_cell.y))
        else:
            print("Moves:", end="")
            print(self.moves)
            for (i, j, reason) in self.moves:
                self.check_grid(i, j)

            self.moves.clear()
            # self.print_grids()

    def update_all_cells(self):
        for i in range(len(self.ai_cells)):
            for j in range(len(self.ai_cells[i])):
                temp_cell = self.ai_cells[i][j]
                temp_cell.update_safe_neighbors()
                temp_cell.update_hidden_neighbors()
                temp_cell.update_identified_mines()

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
