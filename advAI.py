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
        self.near_mines = 0
        self.count_neighbor_mines()
        self.safe_neighbors = []
        self.identified_mines = []
        self.hidden_neighbors = []

        self.mine_guess = -1
        self.mine_final = -1

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

    def update_all(self):  # Updates three lists based on the given cell's surroundings
        self.safe_neighbors.clear()  # List to identify uncovered adjacent boxes -- denoted as 1
        self.hidden_neighbors.clear()  # List to identify covered adjacent boxes -- denoted as 2
        self.identified_mines.clear()  # List to identify known adjacent mines -- denoted as 3
        if self.x + 1 < self.dim:
            # EAST
            if self.ai_cells[self.x + 1][self.y].status == 1:
                self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y])
            if self.ai_cells[self.x + 1][self.y].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y])
            if self.ai_cells[self.x + 1][self.y].status >= 3:
                self.identified_mines.append(self.ai_cells[self.x + 1][self.y])

            # SOUTHEAST
            if self.y + 1 < self.dim:
                if self.ai_cells[self.x + 1][self.y + 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y + 1])
                if self.ai_cells[self.x + 1][self.y + 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y + 1])
                if self.ai_cells[self.x + 1][self.y + 1].status >= 3:
                    self.identified_mines.append(self.ai_cells[self.x + 1][self.y + 1])

            # NORTHEAST
            if self.y - 1 >= 0:
                if self.ai_cells[self.x + 1][self.y - 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x + 1][self.y - 1])
                if self.ai_cells[self.x + 1][self.y - 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x + 1][self.y - 1])
                if self.ai_cells[self.x + 1][self.y - 1].status >= 3:
                    self.identified_mines.append(self.ai_cells[self.x + 1][self.y - 1])

        if self.x - 1 >= 0:
            # WEST
            if self.ai_cells[self.x - 1][self.y].status == 1:
                self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y])
            if self.ai_cells[self.x - 1][self.y].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y])
            if self.ai_cells[self.x - 1][self.y].status >= 3:
                self.identified_mines.append(self.ai_cells[self.x - 1][self.y])

            # SOUTHWEST
            if self.y + 1 < self.dim:
                if self.ai_cells[self.x - 1][self.y + 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y + 1])
                if self.ai_cells[self.x - 1][self.y + 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y + 1])
                if self.ai_cells[self.x - 1][self.y + 1].status >= 3:
                    self.identified_mines.append(self.ai_cells[self.x - 1][self.y + 1])

            # NORTHWEST
            if self.y - 1 >= 0:
                if self.ai_cells[self.x - 1][self.y - 1].status == 1:
                    self.safe_neighbors.append(self.ai_cells[self.x - 1][self.y - 1])
                if self.ai_cells[self.x - 1][self.y - 1].status == 2:
                    self.hidden_neighbors.append(self.ai_cells[self.x - 1][self.y - 1])
                if self.ai_cells[self.x - 1][self.y - 1].status >= 3:
                    self.identified_mines.append(self.ai_cells[self.x - 1][self.y - 1])

        # SOUTH
        if self.y + 1 < self.dim:
            if self.ai_cells[self.x][self.y + 1].status == 1:  # E
                self.safe_neighbors.append(self.ai_cells[self.x][self.y + 1])
            if self.ai_cells[self.x][self.y + 1].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x][self.y + 1])
            if self.ai_cells[self.x][self.y + 1].status >= 3:
                self.identified_mines.append(self.ai_cells[self.x][self.y + 1])

        # NORTH
        if self.y - 1 >= 0:
            if self.ai_cells[self.x][self.y - 1].status == 1:  # E
                self.safe_neighbors.append(self.ai_cells[self.x][self.y - 1])
            if self.ai_cells[self.x][self.y - 1].status == 2:
                self.hidden_neighbors.append(self.ai_cells[self.x][self.y - 1])
            if self.ai_cells[self.x][self.y - 1].status >= 3:
                self.identified_mines.append(self.ai_cells[self.x][self.y - 1])

    def count_neighbors(self):  # Used for safety detection
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


class Constraint:
    def __init__(self, cells, sum):
        self.cells = cells
        self.sum = sum


class AdvAIBrain:
    def __init__(self, map, dim, num_mines):
        self.dim = dim
        self.map = map
        self.num_mines = num_mines
        self.ai_cells = [[0] * dim for i in range(dim)]
        self.init_ai_cells()
        self.moves = []
        self.fringe = []
        self.constraints = []
        self.cnt = 0
        self.possible_sol = []

    def init_ai_cells(self):
        for x in range(self.dim):
            for y in range(self.dim):
                self.ai_cells[x][y] = AICell(x, y, 2, self.dim, self.map,
                                             None)  # Get clue value, initialize lists for neighbor knowns/unknowns
        for x in range(self.dim):
            for y in range(self.dim):
                self.ai_cells[x][y].ai_cells = self.ai_cells

    def check_grid(self, xval, yval):
        if self.map.visit.grid[xval][yval] == 0:
            fill = "Green"
            text = str(self.map.clue.getClue(xval, yval))

            if self.map.grid[xval][yval] == self.map.mine:
                fill = "Red"
                text = "GG"

            if self.ai_cells[xval][yval].status == 3:
                fill = "salmon"
                text = "Flag"

            self.map.canvas.itemconfig(self.map.gui_grid[yval][xval], fill=fill)
            self.map.canvas.itemconfig(self.map.gui_text[yval][xval], text=text,
                                       font=("Papyrus", int(32 / math.log(self.dim, 2))), fill='Black')

            if fill == "Green":
                self.ai_cells[xval][yval].status = 1  # Set to uncovered
                self.map.visit.setVisited(xval, yval)  # Update map

            if fill == "Red":
                self.ai_cells[xval][yval].status = 4  # Set to exploded
                self.map.visit.setVisited(xval, yval)  # Update map

    def update_all_cells(self):
        for x in range(len(self.ai_cells)):
            for y in range(len(self.ai_cells[0])):
                # if self.ai_cells[x][y].status == 1:
                self.ai_cells[x][y].update_all()

    def assess_knowledge(self):
        self.update_all_cells()
        for x in range(len(self.ai_cells)):
            for y in range(len(self.ai_cells[0])):
                temp_cell = self.ai_cells[x][y]
                if temp_cell.status == 1:  # If cell is uncovered
                    if temp_cell.near_mines - len(temp_cell.identified_mines) == len(temp_cell.hidden_neighbors):
                        # if clue - known adjacent mines = covered squares left
                        # Every hidden neighbor is a mine
                        for i in range(len(temp_cell.hidden_neighbors)):
                            temp_cell.hidden_neighbors[i].status = 3
                            self.moves.append(
                                (temp_cell.hidden_neighbors[i].x, temp_cell.hidden_neighbors[i].y, "mine"))

                    self.update_all_cells()
                    if (temp_cell.count_neighbors() - temp_cell.near_mines) - len(temp_cell.safe_neighbors) == len(
                            temp_cell.hidden_neighbors):
                        # if (all adjacents - clue) - all uncovered adjacents = covered squares left
                        # Every hidden neighbor is safe
                        for i in range(len(temp_cell.hidden_neighbors)):
                            temp_cell.hidden_neighbors[i].status = 1
                            self.moves.append(
                                (temp_cell.hidden_neighbors[i].x, temp_cell.hidden_neighbors[i].y, "safe"))

    # Produces a fringe: A fringe is the set of variables that surround all non-covered cells.
    def produce_fringe_and_constraints(self):
        self.fringe.clear()
        self.constraints.clear()
        self.possible_sol.clear()
        self.update_all_cells()
        for i in range(len(self.ai_cells)):
            for j in range(len(self.ai_cells[i])):
                curr = self.ai_cells[i][j]
                if curr.status == 1 and len(curr.hidden_neighbors) > 0:
                    # print(curr.x, curr.y)
                    self.fringe.extend(self.add_to_fringe(curr))
                    self.produce_constraints(curr)
        # self.print_cell_list(self.fringe)

    def add_to_fringe(self, cell):
        distinct_list = []
        for idx in range(len(cell.hidden_neighbors)):
            if cell.hidden_neighbors[idx] in self.fringe:
                continue
            # cell.hidden_neighbors[idx].fringe_sum = cell.near_mines
            distinct_list.append(cell.hidden_neighbors[idx])
        return distinct_list

    def produce_constraints(self, cell):
        self.constraints.append(Constraint(cell.hidden_neighbors, (cell.near_mines - len(cell.identified_mines))))

    # Walks through all possible combinations of solutions to the fringe variables, stores non-pruned solutions
    def backtracking(self, idx):
        if idx == len(self.fringe):
            temp = self.store_fringe_guesses()
            if len(temp) != 0:
                self.possible_sol.append(temp)
            # self.mark_consistent()
            return
        if self.fringe[idx].mine_guess != -1:
            return self.backtracking(idx + 1)
        for i in range(0, 2):
            self.fringe[idx].mine_guess = i
            if self.satisfies_constraints():
                if self.backtracking(idx + 1):
                    return True
                self.fringe[idx].mine_guess = -1

    # Checks currently initialized guesses by the backtracking algorithm to prune paths that violate any constraints.
    def satisfies_constraints(self):
        for i in range(len(self.constraints)):
            curr_constraint = self.constraints[i]
            temp_sum = 0
            skip_constraint = False
            for j in range(len(curr_constraint.cells)):
                constraint_cell = curr_constraint.cells[j]

                # if this constraint involves an unassigned fringe variable move forward to next constraint.
                # no meaningful info can be drawn from this constraint yet
                if constraint_cell.mine_guess == -1:
                    skip_constraint = True
                    break

                # otherwise add to running total mines to see if it is consistent with constraint sum.
                temp_sum = temp_sum + constraint_cell.mine_guess
            if skip_constraint:
                continue
            # final calculated mines were not consistent with constraint's expected sum, constraint was not satisfied.
            if temp_sum != curr_constraint.sum:
                return False
        return True

    def perform_query(self):
        self.assess_knowledge()
        self.cnt = 0
        self.produce_fringe_and_constraints()
        self.backtracking(0)
        self.mark_consistent()
        self.check_answer()

        if len(self.moves) == 0:  # After assessing all knowns, no hidden cell can be marked as a mine or safe
            self.pick_random_cell()
        else:
            print("Moves:", end="")
            print(self.moves)
            for (i, j, idx) in self.moves:
                self.check_grid(i, j)
            self.moves.clear()

    # returns randomly picked cell, None if no cell was picked.
    def pick_random_cell(self):
        covered = []
        for i in range(len(self.ai_cells)):  # Generate list of all unknown cells
            for j in range(len(self.ai_cells[0])):
                if self.ai_cells[i][j].status == 2:
                    covered.append(self.ai_cells[i][j])

        # Choose randomly from covered cells
        if len(covered) > 0:
            rand_idx = randint(0, len(covered) - 1)
            rand_cell = covered[rand_idx]
            self.check_grid(rand_cell.x, rand_cell.y)
            print("Testing random cell: " + str(rand_cell.x) + " " + str(rand_cell.y))
            return rand_cell
        return None

    def store_fringe_guesses(self):
        temp = []
        for i in range(len(self.fringe)):
            temp.append(self.fringe[i].mine_guess)
        return temp

    def mark_consistent(self):
        if len(self.possible_sol) == 0:
            return

        orig = self.possible_sol[0]

        for i in range(len(self.possible_sol)):
            for j in range(len(self.possible_sol[i])):
                # if value changed, set to some error num -2
                if orig[j] != self.possible_sol[i][j]:
                    orig[j] = -2

        for i in range(len(orig)):
            if orig[i] != -2:
                self.fringe[i].mine_final = orig[i]

    def check_answer(self):
        # print("len of fringe: " + str(len(self.fringe)))
        for i in range(len(self.fringe)):
            if self.fringe[i].mine_final == 1:
                self.fringe[i].status = 3
                self.moves.append((self.fringe[i].x, self.fringe[i].y, "dfs1"))
            if self.fringe[i].mine_final == 0:
                self.fringe[i].status = 1
                self.moves.append((self.fringe[i].x, self.fringe[i].y, "dfs0"))

