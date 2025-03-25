# Write your code here :-)
import heapq
import copy

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def enqueue(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def dequeue(self):
        return heapq.heappop(self.elements)[1]

    def is_empty(self):
        return len(self.elements) == 0


class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start to current node
        self.h = h  # Manhattan Distance heuristic
        self.f = g + h  # Total cost

    def __lt__(self, other):
        return self.f < other.f  # Needed for priority queue

    def __str__(self):
        return str(self.state)


class PuzzleSolver:
    GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Solved puzzle state

    def __init__(self, start):
        self.start = start

    def heuristic(self, state):
        """ Manhattan Distance: Sum of vertical & horizontal moves needed to reach goal positions. """
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:  # Ignore the empty tile (0)
                    target_x, target_y = divmod(value - 1, 3)  # Compute goal position
                    distance += abs(target_x - i) + abs(target_y - j)
        return distance

    def find_space(self, state):
        """ Find the position of the empty space (0). """
        for row in range(3):
            for col in range(3):
                if state[row][col] == 0:
                    return row, col

    def find_moves(self, pos):
        #x, y = pos
        #return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        #Generate valid moves for the empty space.
        x, y = pos
        moves = []
        if x > 0: moves.append((-1, 0))  # Move Up
        if x < 2: moves.append((1, 0))   # Move Down
        if y > 0: moves.append((0, -1))  # Move Left
        if y < 2: moves.append((0, 1))   # Move Right
        return moves

    def is_valid(self, move, state):
        """ Check if a move is within bounds of the puzzle. """
        x, y = move
        return 0 <= x < len(state) and 0 <= y < len(state[0])

    def play_move(self, state, move, space):
        """ Generate a new state after making a move. """
        space_x, space_y = space
        #move_x, move_y = move
        move_x, move_y = space_x + move[0], space_y + move[1]
        new_state = copy.deepcopy(state)
        new_state[space_x][space_y], new_state[move_x][move_y] = new_state[move_x][move_y], new_state[space_x][space_y]
        return new_state

    def solve_puzzle(self):
        """ A* Search Algorithm using Manhattan Distance heuristic. """
        start_node = Node(self.start, None, 0, self.heuristic(self.start))
        pq = PriorityQueue()
        pq.enqueue(start_node, start_node.f)
        explored = set()

        while not pq.is_empty():
            current = pq.dequeue()
            explored.add(str(current.state))

            if current.state == self.GOAL_STATE:
                return self.get_solution_path(current)

            space_pos = self.find_space(current.state)
            for move in self.find_moves(space_pos):
                new_state = self.play_move(current.state, move, space_pos)
                if str(new_state) not in explored:
                    new_node = Node(new_state, current, current.g + 1, self.heuristic(new_state))
                    pq.enqueue(new_node, new_node.f)

        return None  # No solution found

    def get_solution_path(self, node):
        """ Reconstruct the path from goal to start. """
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]  # Reverse to get start-to-goal order

    def print_solution(self, solution):
        """ Print the solution path step by step. """
        if solution:
            print("\nSolution Path:")
            for step, state in enumerate(solution, start=1):
                print(f"Step {step}:")
                for row in state:
                    print(" ".join(str(tile) for tile in row))
                print("\n")
        else:
            print("No solution found.")


# Running the solver
ps = PuzzleSolver([[4, 7, 8], [3, 6, 5], [1, 2, 0]])
solution = ps.solve_puzzle()
ps.print_solution(solution)
