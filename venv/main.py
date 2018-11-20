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
        for j in range(0, splitted_pos):
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
    if zero_index > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - 1])
    if zero_index < board_size*board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + 1])
    if zero_index - board_size > 0:
        neighbors.insert(len(neighbors), splitted_position[zero_index - board_size])
    if zero_index + board_size < board_size*board_size - 1:
        neighbors.insert(len(neighbors), splitted_position[zero_index + board_size])


    return createPositionsFromNeighbors(neighbors, position)


def IDSMainFunc(depth, initial_pos, goal, board_size):
    open_list = [initial_pos]
    current = None
    for i in range(0, depth+1):
        print current
        current = open_list[-1]
        del open_list[-1]
        if current == goal:
            return 1
        else:
            n = getNeighbors(current, board_size)
            for j in range(0, len(n)):
                open_list.insert(len(open_list), n[j])
    return 0




def IDS(initial_position, goal, board_size):
    print 'IDS'
    depth = 0
    stop = 0
    while(stop == 0):
        stop = IDSMainFunc(depth, initial_position, goal, board_size)
        depth += 1



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
    '''
    initial_position = lines[2].split('-')
    addition = 0
    board =  [[None for col in range(board_size)] for row in range(board_size)]
    for i in range(0, board_size):
        for j in range(0,board_size):
            board[i][j] = initial_position[addition + j]
        addition += board_size
    '''
    if lines[0] == '1':
        IDS(initial_position, goal_state, board_size)
    elif lines[0] == '2':
        BFS(initial_position)
    elif lines[0] == '3':
        AStar(initial_position)
    else:
        print 'algorithm number should be integer between 1 to 3'
        return


if __name__ == "__main__":
    main()