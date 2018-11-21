import sys
#Efrat Sofer 304855125

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
    # right neighbor
    if zero_index < board_size*board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + 1])
    # bottom neighbor
    if zero_index + board_size < board_size*board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + board_size])
    # left neighbor
    if zero_index > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - 1])

    return createPositionsFromNeighbors(neighbors, position)



def DLS(src, target, limit, board_size):
    if src == target:
        return True
    if limit <= 0:
        return False
    neighbors = getNeighbors(src, board_size)
    for n in neighbors:
        if DLS(n, target, limit - 1, board_size):
            return True
    return False


def IDDFS(src, target, max_depth, board_size):
    for limit in range(0, max_depth):
        print 'begin depth: ' + str(limit)
        if DLS(src, target, limit, board_size) == True:
            return True
    return False

def BFS(board):
    print 'BFS'

def AStar(board):
    print 'AStar'


def main():
    if len(sys.argv) != 2:
        print 'the program needs one input argument'
        return
    input_file_name = sys.argv[1]
    f_input = open(input_file_name, "r")
    lines = f_input.read().splitlines()
    try:
        board_size = int(lines[1])
    except ValueError:
        print 'board size is not a valid integer'
        return
    initial_position = lines[2]
    goal_state = getGoalState(board_size)

    if lines[0] == '1':
        IDDFS(initial_position, goal_state, board_size, board_size)
        #IDS(initial_position, goal_state, board_size)
    elif lines[0] == '2':
        BFS(initial_position)
    elif lines[0] == '3':
        AStar(initial_position)
    else:
        print 'algorithm number should be integer between 1 to 3'
        return


if __name__ == "__main__":
    main()
