class Node:
    def __init__(self, state, parent=None):
        # Store the node state and parent state
        self.state = state
        self.parent = parent

    def __str__(self):
        # Implement a method to print the state of the node
        state = ""
        for i in self.state:
            state += " ".join(str(j) for j in i) + "\n"
        return state

    def __repr__(self):
        return self.__str__()

class PuzzleSolver:
    def __init__(self, start, goal):
        # Initialize the puzzle with start and goal state
        self.start = start
        self.goal = goal
        self.visited = set()  # Track visited states for backtracking

    def is_solvable (self, state):
        # Check if the puzzle state is solvable
        array = []
        for row in state:
            for tile in row:
                if tile != ' ':
                    array.append(tile)

        inversion_count = 0
        for i in range(len(array)):
            for j in range(i+1,len(array)):
                if array[i] and array[j] and array[i] > array[j]:
                    inversion_count+=1
        return inversion_count % 2 == 0

    def find_space(self, state):
        # Implement the method to find the position (x, y) of the empty space (' ')
        for row in range(len(state)):
            for tile in range(len(state[0])):
                if (state[row][tile] == ' '):
                    return (row,tile)
        #return None  # Should not happen, but good practice to handle

    def find_moves(self, pos):
        # Implement the method to generate valid moves for the empty space
        x, y = pos
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    def is_valid(self, move, state):
        # Implement the method to check if a move is within bounds of the puzzle
        x,y = move
        return 0 <= x < len(state) and 0 <= y < len(state[0])

    def play_move(self, state, move, space):
        # Implement the method to generate a new state after making the move
        space_x , space_y = space
        move_x , move_y = move
        new_state = copy.deepcopy(state)
        for row in range(len(state)):
            for tiles in range (len(state[0])):
                new_state[row][tiles] = state[row][tiles]
        #print(new_state)
        new_state[space_x][space_y], new_state[move_x][move_y] = new_state[move_x][move_y], new_state[space_x][space_y]
        return new_state

    def generate_children(self, state):
        # Implement the method to generate all valid children from a state
        children = []
        space = self.find_space(state)
        moves = self.find_moves(space)

        for move in moves:
            if self.is_valid(move,state):
                child = self.play_move(state,move,space)
                children.append(child)
        return children

    def solve_puzzle_backtracking(self):
        # Implement the search strategy for simple backtracking

        def backtrack(node):

            def backtrack(state, path):
                if state == self.goal.state:
                    return path

                self.visited.add(str(state))  # Mark state as visited

                for child in self.generate_children(state):
                    if str(child) not in self.visited:
                        result = backtrack(child, path + [child])
                        if result:
                            return result

                return None  # No solution found

            print("Solving with Backtracking...")
            path = backtrack(self.start.state, [self.start.state])

            if path:
                self.disp_solution(path)
            else:
                print("No solution found using Backtracking!")

    def solve_puzzle_dfs(self):
        # Implement the search strategy for simple depth-first-search
        print("Solving with DFS...")
        open_list = [self.start]    # Stack (LIFO) containing the start node
        closed_list = []            # List to store visited states
        while open_list:
            node = open_list.pop()
            if self.is_goal(node.state):
                print("Goal state reached!")
                self.disp_solution(node)   # for displaying all the states that are encountered between
                return node
            elif node.state not in closed_list:
                closed_list.append(node.state)
                childs = self.generate_children(node.state)
                for child in childs:
                        if child not in closed_list:
                            open_list.append(Node(child,node))
        print("No solution found!")

    def solve_puzzle_bfs(self):
        # Implement the search strategy for breadth-first-search
        print("Solving with BFS...")
        open_list = [self.start]     # Queue (FIFO) containing the start node
        #print(open_list)
        closed_list = []             # List to store visited states

        while open_list:
            node = open_list.pop(0)  # Remove the first added node (FIFO behavior)
            if self.is_goal(node.state):
                print("Goal state reached!")
                self.disp_solution(node) #for displaying all the states that are encountered between
                return node
            elif node.state not in closed_list:
                closed_list.append(node.state)
                childs = self.generate_children(node.state)
                for child in childs :
                    if child not in closed_list:
                        open_list.append(Node(child, node))

        print("No solution found!")
        return None

    def solve_puzzle_dfid(self):
        # Implement the search strategy for depth-first-search with iterative deepening
        print("Solving with DFID...")
        def dls(node, depth):
            if node.state == self.goal.state:
                self.disp_solution(node)
                return node
            if depth == 0:
                return None

            for child_state in self.generate_children(node.state):
                child = Node(child_state, node)
                res = dls(child, depth - 1)
                if res:
                    return res
            return None

        # Call dls function iteratively and search
        depth = 0
        while True:
            res = dls(self.start, depth)
            if res:
                return res
            depth += 1

    def disp_solution(self, final_state):
        # Implement the method to display the solution path
        path_states = []
        while final_state:
            path_states.insert(0, final_state)
            final_state = final_state.parent
        print("\nSolution Path:")
        i=1
        for step in path_states:
            print(f"step {i}")
            print(step)
            i+=1

    def is_goal(self, current_state):
      return current_state == self.goal.state

#Run this Test-Case

def main ():
    start = Node([[4, 7, 8], [3, 6, 5], [1, 2, ' ']])
    #goal_state = Node([[7, 6, 5], [8, ' ', 4], [1, 2, 3]])
    #goal_state = Node([[1, 2, 3], [4, 5, 6], [7, 8, ' ']])
    #goal_state = Node([[4, 7, 8], [3, ' ', 6], [1, 2, 5]])
    goal_state = Node([[' ', 7, 8],[4, 3, 6],[1, 2, 5]])

    solver = PuzzleSolver(start,goal_state)
    print("START STATE")
    print(start)
    solver = PuzzleSolver(start,goal_state)
    print("IS SOLVABLE?")
    print(solver.is_solvable(start.state),'\n')
    print("FINDING THE POSITION OF SPACE")
    s = solver.find_space(start.state)
    print(s,'\n')
    print("FINDING ALL MOVES POSSIBLE AGAINST THE SPACE")
    print(solver.find_moves(s),'\n')
    print("GENERATING CHILDREN OF START STATE")
    print(solver.generate_children(start.state),'\n')
    #==========================================================================
    if solver.is_solvable(start.state):
        #print(solver.solve_puzzle_dfs())
        #print(solver.solve_puzzle_bfs())
        print(solver.solve_puzzle_dfid())
        #print(solver.solve_puzzle_backtracking())
    else:
      print("Puzzle is not solveable")
main()
