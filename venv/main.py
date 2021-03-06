import sys
import collections
#Efrat Sofer 304855125
####### node class ##########
''' 
describes a node in a graph, contains attributes: state, parent node, visited boolean, h & g for the A* algorithm 
'''
class Node:
    def __init__(self):
        self.visited = 0
        self.state = ''
        self.parent = None
        self.g = 0
        self.h = 0
        self.depth = 0
    def setVisited(self, value):
        self.visited = value
    def setState(self, s):
        self.state = s
    def setParent(self, p):
        self.parent = p
    def setG(self, w):
        self.g += w
    def setH(self, value):
        self.h = value
    def setDepth(self, value):
        self.depth = value

####### pririty queue for A* ##########
'''
A simple implementation of Priority Queue using Queue.
i based the code on this implementation:
https://www.geeksforgeeks.org/priority-queue-in-python/
removeFront method removes according to minimum value priority (because we want the path with the min cost)
'''
class PriorityQueue(Node):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == []

        # for inserting an element in the queue

    def insert(self, data):
        self.queue.append(data)

        # for popping an element based on Priority

    def removeFront(self):
        try:
            min_ind = 0
            min_value = self.queue[0].g + self.queue[0].h
            g_plus_h = 0
            for i in range(len(self.queue)):
                g_plus_h = self.queue[i].g + self.queue[i].h
                if g_plus_h < min_value:
                    min_value = g_plus_h
                    min_ind = i
            item = self.queue[min_ind]
            del self.queue[min_ind]
            return item
        except IndexError:
            print()
            exit()


####### general methods ##########
''' 
returns a goal state according to the board size
the goal defined as all the numbers from 1 to (board_size)^2 -1 and the 0 in the end
'''
def getGoalState(board_size):
    result = ''
    for i in range(1, board_size*board_size+1):
        if i != (board_size*board_size):
            result += str(i) + '-'
        else:
            result += '0'
    return result

''' 
creates a position separated by hyphen ('-') to the neighbor nodes of a given node
'''
def createPositionsFromNeighbors(n, original_pos):
    positions = []
    splitted_pos = original_pos.split('-')
    index_of_zero = splitted_pos.index('0')
    for i in range(0, len(n)):
        splitted_pos = original_pos.split('-')
        new_pos = ''
        temp_ind = splitted_pos.index(n[i])
        splitted_pos[index_of_zero] = n[i]
        splitted_pos[temp_ind] = '0'
        for j in range(0, len(splitted_pos)):
            if j < len(splitted_pos) - 1:
                new_pos += splitted_pos[j] + '-'
            else:
                new_pos += splitted_pos[j]
        positions.append(new_pos)

    return positions
''' 
finds the neighbor values of a given node
'''
def getNeighbors(position, board_size):
    neighbors = []
    [row, col] = getRowAndColIndInMatrix(position, board_size, '0')
    splitted_position = position.split('-')
    zero_index = splitted_position.index('0')
    # top neighbor
    if row < board_size-1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + board_size])
    # bottom neighbor
    if row > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - board_size])
    # left neighbor (right neighbor can move to the left into the empty position)
    if col < board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + 1])
    # right neighbor (left neighbor can move to the right into the empty position)
    if col > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - 1])

    return createPositionsFromNeighbors(neighbors, position)

''' 
returns the path moves (U, D, L, R)
'''
def getPath(solution_list, board_size):
    if len(solution_list) < 2:
        return
    path = []
    for i in range(1, len(solution_list)):
        next = solution_list[i].split('-')
        prev = solution_list[i-1].split('-')
        zero_ind_next = next.index('0')
        zero_ind_prev = prev.index('0')
        if zero_ind_next - zero_ind_prev == 1:
            path.append('L')
        elif zero_ind_next - zero_ind_prev == -1:
            path.append('R')
        elif zero_ind_next - zero_ind_prev == board_size:
            path.append('U')
        elif zero_ind_next - zero_ind_prev == -board_size:
            path.append('D')
    return path


#######IDS##########
''' 
the recursive function of IDS
when the goal is found, it adds the node to the solution list
'''
def DFS(start, target, max_depth, neighbors_dict, board_size, vertex_counter_ids):
    depth = 0
    open_list = []
    start.setDepth(depth)
    open_list.append(start)
    current = None
    stop = False
    while not stop:
        if len(open_list) == 0:
            return [False]
        current = open_list.pop()
        vertex_counter_ids += 1
        if current.state == target.state:
            result = []
            result = getPathFromLastNodeBfs(current)
            result.insert(0, [True])
            result.append(vertex_counter_ids)
            return result
        if current.depth + 1 <= max_depth:
            neighbors = getNeighbors(current.state, board_size)
            neighbors.reverse()
            for n in neighbors:
                n_node = Node()
                n_node.setState(n)
                n_node.setParent(current)
                n_node.setDepth(current.depth + 1)
                open_list.append(n_node)
    return [False]


''' 
the function that calls the DLS function with a given depth
'''
def IDDFS(src, target, board_size):
    n_dict = {}
    for limit in range(0, 10000000):
        node_src = Node()
        node_src.setParent(None)
        node_src.setState(src)
        node_target = Node()
        node_target.setState(target)
        solution = []
        vertex_counter_ids = 0
        print ('begin depth: ' + str(limit))
        result = DFS(node_src, node_target, limit, n_dict, board_size, vertex_counter_ids)
        if result[0]:
            print ('found solution in IDS')
            path = getPath(result[1], board_size)
            return [path, result[-1], limit]
    return []


#######BFS##########
''' 
returns a path of states & path of nodes from a given last node
'''
def getPathFromLastNodeBfs(last_node):
    result = [last_node.state]
    result_nodes = [last_node]
    stop = False
    prev = last_node
    while stop == False:
        vertex = prev.parent
        if vertex != None:
            result.append(vertex.state)
            result_nodes.append(vertex)
            prev = vertex
        else:
            stop = True
    result.reverse()
    result_nodes.reverse()
    return [result, result_nodes]


''' 
the BFS algorithm - transverses all children in the same level before continuing to the next
'''
def BFS(board_size, root, goal):
    root_node = Node()
    root_node.setState(root)
    root_node.setParent(None)
    queue = collections.deque([root_node])
    number_of_verteces_checked = 0
    while queue:
        vertex = queue.popleft()
        #vertex_node = Node()
        #vertex_node.setState(vertex)
        number_of_verteces_checked += 1
        if vertex.state == goal:
            print ('found solution for BFS! number of verteces checked: ' + str(number_of_verteces_checked))
            [path_states, path_nodes] = getPathFromLastNodeBfs(vertex)
            path = getPath(path_states, board_size)
            return [path, number_of_verteces_checked, 0]
        neighbors = getNeighbors(vertex.state, board_size)
        for n in neighbors:
            n_node = Node()
            n_node.setState(n)
            n_node.setParent(vertex)
            queue.append(n_node)


####### A* ##########
''' 
return index of an element(state) in the matrix,
for example if the board_size is 3*3
and we have the state 1-2-3-4-5-6-7-8-0 and we want to know the row&col index of '4', it
will return row 1 and column 0 
'''
def getRowAndColIndInMatrix(state, board_size, element):
    splitted_state = state.split('-')
    index_of_element = splitted_state.index(element)
    col_index = index_of_element%board_size
    row_index = 0
    counter_top = -1
    for i in range(0, board_size):
        counter_top += board_size
        if index_of_element <= counter_top:
            row_index = i
            break
    return [row_index, int(col_index)]


''' 
manhattan heuristic function 
'''
def calculateHeuristic(state, goal, board_size):
    splitted_state = state.split('-')
    manhattan_dist = 0
    for i in range(0, len(splitted_state)):
        if splitted_state[i] == '0':
            continue
        [row_s, col_s] = getRowAndColIndInMatrix(state, board_size, splitted_state[i])
        [row_g, col_g] = getRowAndColIndInMatrix(goal, board_size, splitted_state[i])
        manhattan_dist += abs(row_s - row_g) + abs(col_s - col_g)

    return manhattan_dist

''' 
in the given assignment each edge has the same weight - 1, so returns the length of the path nodes minus 1
'''
def calculatePathCost(path_nodes):
    return (len(path_nodes)-1)

''' 
A star main function implementation
'''
def AStar(initial, goal, board_size):
    neighbors_dict = {}
    heuristic_dict = {}
    depth = 0
    num_vertex_checked = 0
    node_initial = Node()
    node_initial.setState(initial)
    node_initial.setParent(None)
    #node_initial.setInitialG()
    evaluated_heuristic = calculateHeuristic(initial, goal, board_size)
    heuristic_dict[initial] = evaluated_heuristic
    node_initial.setH(evaluated_heuristic)
    node_initial.setG(depth)
    #node_goal = Node()
    #node_goal.setState(goal)
    open_list = PriorityQueue()
    open_list.insert(node_initial)
    while not open_list.isEmpty():
        current_node = open_list.removeFront()
        num_vertex_checked += 1
        if current_node.state == goal:
            [path_states, path_nodes] = getPathFromLastNodeBfs(current_node)
            path = getPath(path_states, board_size)
            cost = calculatePathCost(path_nodes)
            return [path, num_vertex_checked, cost]
        if current_node.state in neighbors_dict:
            neighbors = neighbors_dict[current_node.state]
        else:
            neighbors = getNeighbors(current_node.state, board_size)
            neighbors_dict[current_node.state] = neighbors
        for n in neighbors:
            n_node = Node()
            n_node.setState(n)
            n_node.setParent(current_node)
            #n_node.setInitialG()
            n_node.setG(current_node.g + 1)
            if n_node.state in heuristic_dict:
                evaluated_heuristic = heuristic_dict[n_node.state]
            else:
                evaluated_heuristic = calculateHeuristic(n, goal, board_size)
                heuristic_dict[n_node.state] = evaluated_heuristic
            n_node.setH(evaluated_heuristic)
            open_list.insert(n_node)
    return False

''' 
the function that calls A star, returns an empty list if solution wasn't found
'''
def operateAStar(initial, goal, board_size):
    solution = AStar(initial, goal, board_size)
    if len(solution) > 0:
        print('found solution in A*!!')
        return solution
    else:
        return []

####### main function ##########
''' 
the main function: reads the input, calls the suitable function & writes to the output
'''
def main():
    input_file_name = 'input.txt'
    input_file_name = sys.argv[1]
    f_input = open(input_file_name, 'r')
    lines = f_input.read().splitlines()
    try:
        board_size = int(lines[1])
    except ValueError:
        print ('board size is not a valid integer')
        return
    initial_position = lines[2]
    goal_state = getGoalState(board_size)
    solution = []
    if lines[0] == '1':
        solution = IDDFS(initial_position, goal_state, board_size)
        #IDS(initial_position, goal_state, board_size)
    elif lines[0] == '2':
        solution = BFS(board_size, initial_position, goal_state)
    elif lines[0] == '3':
        solution = operateAStar(initial_position, goal_state, board_size)
    else:
        print('algorithm number should be integer between 1 to 3')
        return
    if len(solution) == 3:
        path = solution[0]
        string_path = ''
        for i in range(0, len(path)):
            string_path += path[i]
        s = string_path + ' ' + str(solution[1]) + ' ' + str(solution[2])
        print(s)
        f_output = open('output', 'w')
        f_output.write(s)



if __name__ == "__main__":
    main()
