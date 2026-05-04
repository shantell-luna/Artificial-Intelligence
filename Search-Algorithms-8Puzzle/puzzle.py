from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        # Cannot move up if blank tile is in the first row
        if self.blank_index < self.n:
            return None
        
        swap_index = self.blank_index - self.n
        new_config = self.config[:]
        temp = new_config[self.blank_index]
        new_config[self.blank_index] = new_config[swap_index]
        new_config[swap_index] = temp
        return PuzzleState(new_config, self.n, parent=self, action="Up", cost=self.cost + 1)
    
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        # Cannot move down if blank tile is in the last row
        if self.blank_index >= (self.n * (self.n - 1)):
            return None
        
        swap_index = self.blank_index + self.n
        new_config = self.config[:]
        temp = new_config[self.blank_index]
        new_config[self.blank_index] = new_config[swap_index]
        new_config[swap_index] = temp
        return PuzzleState(new_config, self.n, parent=self, action="Down", cost=self.cost + 1)

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        # Cannot move left if blank tile is in the first column
        if self.blank_index % self.n == 0:
            return None 
        swap_index = self.blank_index - 1
        new_config = self.config[:]
        temp = new_config[self.blank_index]
        new_config[self.blank_index] = new_config[swap_index]
        new_config[swap_index] = temp
        return PuzzleState(new_config, self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        # Cannot move right if blank tile is in the last column
        if self.blank_index % self.n == (self.n - 1):
            return None
        swap_index = self.blank_index + 1
        new_config = self.config[:]
        temp = new_config[self.blank_index]
        new_config[self.blank_index] = new_config[swap_index]
        new_config[swap_index] = temp
        return PuzzleState(new_config, self.n, parent=self, action="Right", cost=self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_depth, running_time, max_ram_usage):
    ### Student Code Goes here
    with open("output.txt", "w") as f:
        f.write(f"path_to_goal: {path_to_goal}\n")
        f.write(f"cost_of_path: {cost_of_path}\n")
        f.write(f"nodes_expanded: {nodes_expanded}\n")
        f.write(f"search_depth: {search_depth}\n")
        f.write(f"max_search_depth: {max_depth}\n")
        f.write(f"running_time: {running_time:.8f}\n")
        f.write(f"max_ram_usage: {max_ram_usage:.8f}\n")

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    bfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = Q.Queue()
    frontier.put(initial_state)
    frontier_set = {tuple(initial_state.config)}
    explored = set() 
    nodes_expanded = 0
    max_search_depth = 0   

    while not frontier.empty():
        state = frontier.get()
        frontier_set.remove(tuple(state.config))

        if test_goal(state):
            path_to_goal = []
            temp = state

            while state.parent is not None:
                path_to_goal.append(state.action)
                state = state.parent
            path_to_goal.reverse()

            running_time = time.time() - start
            cost_of_path = temp.cost
            search_depth = temp.cost
            bfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - bfs_start_ram) / (2**20)
            writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, bfs_ram)
            return

        explored.add(tuple(state.config))
        nodes_expanded += 1
        
        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_set:
                frontier.put(child)
                frontier_set.add(tuple(child.config))
                max_search_depth = max(max_search_depth, child.cost)
    return

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    dfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = [initial_state]
    frontier_set = {tuple(initial_state.config)}
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier == []:
        state = frontier.pop()

        if test_goal(state):
            running_time = time.time() - start
            cost_of_path = state.cost
            search_depth = state.cost
            dfs_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram) / (2**20)

            path_to_goal = []
            temp = state
            while temp.parent is not None:
                path_to_goal.append(temp.action)
                temp = temp.parent
            path_to_goal.reverse()

            writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, dfs_ram)
            return

        explored.add(tuple(state.config))
        nodes_expanded += 1

        for child in reversed(state.expand()):
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_set:
                frontier.append(child)
                frontier_set.add(tuple(child.config))
                max_search_depth = max(max_search_depth, child.cost)

    return
                

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    astar_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = Q.PriorityQueue()
    frontier.put((calculate_total_cost(initial_state), id(initial_state), initial_state))
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    frontier_set = {tuple(initial_state.config)}

    while not frontier.empty():
        _, _, state = frontier.get()
        frontier_set.remove(tuple(state.config))

        if test_goal(state):
            running_time = time.time() - start
            cost_of_path = state.cost
            search_depth = state.cost
            astar_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - astar_start_ram) / (2**20)

            path_to_goal = []
            temp = state
            while temp.parent is not None:
                path_to_goal.append(temp.action)
                temp = temp.parent
            path_to_goal.reverse()

            writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, astar_ram)
            return

        explored.add(tuple(state.config))
        nodes_expanded += 1

        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in frontier_set:
                frontier.put((calculate_total_cost(child), id(child), child))
                frontier_set.add(tuple(child.config))
                max_search_depth = max(max_search_depth, child.cost)
    return

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    total = state.cost
    for idx, value in enumerate(state.config):
        total += calculate_manhattan_dist(idx, value, state.n)
    return total

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    if value == 0:
        return 0
    current_row, current_col = divmod(idx, n)
    target_row, target_col = divmod(value, n)
    return abs(current_row - target_row) + abs(current_col - target_col)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    return puzzle_state.config == list(range(puzzle_state.n * puzzle_state.n))

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
