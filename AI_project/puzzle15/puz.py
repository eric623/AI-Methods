# Création de la classe State
class State():
    def __init__(self,board):
        self.board = board
        self.empty_pos = self.find_empty()

    def find_empty(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] ==0:
                    return (i,j)
                
# Fonctions retournant les actions possibles d'un state donné <>
def action(state):
    i,j=state.empty_pos
    actions = []
    if i> 0: actions.append("UP")
    if i<3 : actions.append("DOWN")
    if j>0 : actions.append("LEFT")
    if j<3 : actions.append("RIGHT")
    return actions

# Modèle de transition :
def result(s,a):
    new_board = [row[:] for row in s.board]
    i,j=s.empty_pos
    if a=="UP" : new_board[i][j],new_board[i-1][j]=new_board[i-1][j],new_board[i][j]
    elif a == "DOWN":
        new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
    elif a == "LEFT":
        new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
    elif a == "RIGHT":
        new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
    return State(new_board)

# Fonction goal
def goal_test(s):
    goal = [[1,2,3,4],
            [5,6,7,8],
            [9,10,11,12],
            [13,14,15,0]]
    return s.board==goal

# Classe Node
class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

# Résolution du problème
import heapq

def heuristic(state):
    goal_pos = {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}
    return sum(abs(i - goal_pos[val][0]) + abs(j - goal_pos[val][1])
               for i, row in enumerate(state.board) for j, val in enumerate(row) if val)

def a_star_search(initial_state):
    frontier = [(heuristic(initial_state), 0, Node(initial_state))]
    explored = set()
    
    while frontier:
        _, cost, node = heapq.heappop(frontier)

        if goal_test(node.state):
            actions = []
            while node.parent:
                actions.append(node.action)
                node = node.parent
            return actions[::-1]

        explored.add(tuple(map(tuple, node.state.board)))

        for action in action(node.state):
            new_state = result(node.state, action)
            new_node = Node(new_state, node, action, cost + 1)
            if tuple(map(tuple, new_state.board)) not in explored:
                heapq.heappush(frontier, (cost + heuristic(new_state), cost + 1, new_node))

    return None
