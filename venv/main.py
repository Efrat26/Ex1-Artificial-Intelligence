import sys

#Efrat Sofer 304855125

def IDSMainFunc(depth):
    open_list = []
    for i in range(0, depth+1):
        open_list[i] = 0

def IDS(initial_pos, board):
    print 'IDS'
    depth = 0
    stop = 0
    while(stop == 0):
        stop = IDSMainFunc(depth)
        depth += 1



def BFS(initial_pos):
    print 'BFS'

def AStar(initial_pos):
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
    initial_position = lines[2].split('-')
    addition = 0
    board =  [[None for col in range(board_size)] for row in range(board_size)]
    for i in range(0, board_size):
        for j in range(0,board_size):
            board[i][j] = initial_position[addition + j]
        addition += board_size
    if lines[0] == '1':
        IDS()
    elif lines[0] == '2':
        BFS()
    elif lines[0] == '3':
        AStar()
    else:
        print 'algorithm number should be integer between 1 to 3'
        return


if __name__ == "__main__":
    main()