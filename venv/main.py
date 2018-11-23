import sys
import collections
#Efrat Sofer 304855125

####### node class ##########
class Node:
    def __init__(self):
        visited = 0
        state = ''
        parent = None
    def setVisited(self, value):
        self.visited = value
    def setState(self, s):
        self.state = s
    def setParent(self, p):
        self.parent = p

####### pririty queue for A* ##########
'''
A simple implementation of Priority Queue using Queue.
i used the code from here:
https://www.geeksforgeeks.org/priority-queue-in-python/
'''
class PriorityQueue(object):
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

    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


####### general methods ##########
def getGoalState(board_size):
    result = ''
    for i in range(1,board_size*board_size+1):
        if i != (board_size*board_size):
            result += str(i) + '-'
        else:
            result += '0'
    return result

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

def getNeighbors(position, board_size):
    neighbors = []
    splitted_position = position.split('-')
    zero_index = splitted_position.index('0')
    # top neighbor
    if zero_index - board_size > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - board_size])
    # bottom neighbor
    if zero_index + board_size < board_size*board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + board_size])
    # right neighbor
    if zero_index < board_size * board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + 1])
    # left neighbor
    if zero_index > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - 1])

    return createPositionsFromNeighbors(neighbors, position)


def getPath(solution_list):
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
        elif zero_ind_next - zero_ind_prev == 3:
            path.append('U')
        elif zero_ind_next - zero_ind_prev == -3:
            path.append('D')
    return path


#######IDS##########
def DLS(src, target, limit, board_size, solution_list, vertex_counter, solution):
    if src == target:
        return True
    if limit <= 0:
        return False
    neighbors = getNeighbors(src, board_size)
    for n in neighbors:
        vertex_counter[0] = vertex_counter[0] + 1
        if DLS(n, target, limit - 1, board_size, solution_list, vertex_counter,  solution):
            solution_list.append(n)
            return True
    return False


def IDDFS(src, target, max_depth, board_size):
    for limit in range(0, max_depth):
        solution = [src]
        vertex_num = []
        vertex_num.append(1)
        #vertex_counter = 0
        print ('begin depth: ' + str(limit))
        if DLS(src, target, limit, board_size, solution, vertex_num, solution):
            path = getPath(solution)
            return [path, vertex_num[0], limit]
    return []


#######BFS##########
def getPathFromLastNodeBfs(last_node):
    result = [last_node.state]
    stop = False
    prev = last_node
    while stop == False:
        vertex = prev.parent
        if vertex != None:
            result.append(vertex.state)
            prev = vertex
        else:
            stop = True
    result.reverse()
    return result



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
            path_nodes = getPathFromLastNodeBfs(vertex)
            path = getPath(path_nodes)
            return [path, number_of_verteces_checked, 0]
        neighbors = getNeighbors(vertex.state, board_size)
        for n in neighbors:
            n_node = Node()
            n_node.setState(n)
            n_node.setParent(vertex)
            queue.append(n_node)


####### A* ##########
def getRowAndColIndInMatrix(state, element):
    splitted_state = state.split('-')
    board_size = len(splitted_state)
    board_size_sqrt = board_size ** (1/2.0)
    index_of_element = splitted_state.index(element)
    col_index = index_of_element%board_size_sqrt
    row_index = 0
    counter_top = -1
    for i in range(0, board_size):
        counter_top += board_size_sqrt
        if index_of_element <= counter_top:
            row_index = i
            break
    return [row_index, int(col_index)]



def calculateHeuristic(state, goal, element):
    [row_s, col_s] = getRowAndColIndInMatrix(state, element)
    [row_g, col_g] = getRowAndColIndInMatrix(goal, element)
    result = abs(row_s - row_g) + abs(col_s - col_g)
    return result

def AStar(intial, goal):
    calculateHeuristic(intial, goal)
    print ('AStar')



####### main function ##########
def main():
    if len(sys.argv) != 2:
        print ('the program needs one input argument')
        return
    input_file_name = sys.argv[1]
    f_input = open(input_file_name, "r")
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
        solution = IDDFS(initial_position, goal_state, board_size, board_size)
        #IDS(initial_position, goal_state, board_size)
    elif lines[0] == '2':
        solution = BFS(board_size, initial_position, goal_state)
    elif lines[0] == '3':
        solution = AStar(initial_position, goal_state)
    else:
        print ('algorithm number should be integer between 1 to 3')
        return
    if len(solution) == 3:
        path = solution[0]
        string_path = ''
        for i in range(0, len(path)):
            string_path += path[i]
        print (string_path + ' ' + str(solution[1]) + ' ' + str(solution[2]))



if __name__ == "__main__":
    main()
