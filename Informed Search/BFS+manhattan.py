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
    def __init__(self, state, parent=None, h=0):
        self.state = state
        self.parent = parent
        self.h = h  # Hamming Distance heuristic

    def __lt__(self, other):
        return self.h < other.h  # Greedy: Pick the node with the lowest h(n)

    def __str__(self):
        return str(self.state)


class PuzzleSolver:
    GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Solved puzzle state

    def __init__(self, start):
        self.start = start

    def heuristic(self, state):
        """ Hamming Distance: Count the number of misplaced tiles. """
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != self.GOAL_STATE[i][j]:
                    misplaced += 1
        return misplaced

    def find_space(self, state):
        """ Find the position of the empty space (0). """
        for row in range(3):
            for col in range(3):
                if state[row][col] == 0:
                    return row, col

    def find_moves(self, pos):
        """ Generate valid moves for the empty space. """
        x, y = pos
        moves = []
        if x > 0: moves.append((x - 1, y))  # Move Up
        if x < 2: moves.append((x + 1, y))  # Move Down
        if y > 0: moves.append((x, y - 1))  # Move Left
        if y < 2: moves.append((x, y + 1))  # Move Right
        return moves

    def play_move(self, state, move, space):
        """ Generate a new state after making a move. """
        space_x, space_y = space
        move_x, move_y = move
        new_state = copy.deepcopy(state)
        new_state[space_x][space_y], new_state[move_x][move_y] = new_state[move_x][move_y], new_state[space_x][space_y]
        return new_state

    def solve_puzzle_best_first_search(self):
        """ Best-First Search (Greedy Search) using Hamming Distance heuristic. """
        start_node = Node(self.start, None, self.heuristic(self.start))
        pq = PriorityQueue()
        pq.enqueue(start_node, start_node.h)
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
                    explored.add(str(new_state))  # Avoid revisiting
                    new_node = Node(new_state, current, self.heuristic(new_state))
                    pq.enqueue(new_node, new_node.h)

        return None  # No solution found

    def get_solution_path(self, node):
        """ Reconstruct the path from goal to start. """
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]  # Reverse to get start-to-goal order

    def print_solution(self, solution):
        """ Print the solution path step by step without using enumerate. """
        if solution:
            print("\nSolution Path:")
            step = 1
            for state in solution:
                print(f"Step {step}:")
                for row in state:
                    print(" ".join(str(tile) for tile in row))
                print("\n")
                step += 1
        else:
            print("No solution found.")


# Running the solver
ps = PuzzleSolver([[4, 7, 8], [3, 6, 5], [1, 2, 0]])
solution = ps.solve_puzzle_best_first_search()
ps.print_solution(solution)

