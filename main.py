from node import Node

def swap(successor_board, space, num_pos):
    successor_board.status[space[0]][space[1]], successor_board.status[num_pos[0]][num_pos[1]] = \
        successor_board.status[num_pos[0]][num_pos[1]], successor_board.status[space[0]][space[1]]


def moveLeft(successor_board, space):
    swap(successor_board, space, (space[0], space[1] - 1))


def moveRight(successor_board, space):
    swap(successor_board, space, (space[0], space[1] + 1))


def moveUp(successor_board, space):
    swap(successor_board, space, (space[0] - 1, space[1]))


def moveDown(successor_board, space):
    swap(successor_board, space, (space[0] + 1, space[1]))


def findSpace(status_board):
    space = ()

    for i in range(len(status_board.status)):
        for j in range(len(status_board.status[i])):
            if status_board.status[i][j] == 'm':
                space = (i, j)
    return space


def copyBoard(board):
   return [row[:] for row in status_board.status]


def setNode(status_board, operator):
    successor_board = Node(copyBoard(status_board.status))
    successor_board.parent = status_board
    successor_board.steps_gx = successor_board.parent.steps_gx + 1
    successor_board.current_operator = operator


# https://github.com/boppreh/keyboard/blob/master/README.md
# https://github.com/boppreh/keyboard#keyboardeventname
def operators(status_board):
    space = findSpace(status_board)
    nodes_list = []

    if canMoveLeft(space):
        successor_board = setNode(status_board, "left")
        nodes_list.append(successor_board)
        moveLeft(successor_board, space)

    if canMoveRight(space, successor_board):
        successor_board = setNode(status_board, "right")
        nodes_list.append(successor_board)
        moveRight(successor_board, space)

    if canMoveUp(space):
        successor_board = setNode(status_board, "up")
        nodes_list.append(successor_board)
        moveUp(successor_board, space)

    if canMoveDown(space, successor_board):
        successor_board = setNode(status_board, "down")
        nodes_list.append(successor_board)
        moveDown(successor_board, space)

    return nodes_list


def canMoveLeft(space):
    return space[1] > 0


def canMoveRight(space, board):
    return space[1] < len(board.status[0]) - 1


def canMoveUp(space):
    return space[0] > 0


def canMoveDown(space, board):
    return space[0] < len(board.status) - 1


def findBestStatus(nodes_list):
    pass


def countTiles(status_board, final_board):
    wrong_tiles = 0
    for i in range(len(status_board.status)):
        for j in range(len(status_board.status[i])):
            if status_board.status[i][j] != 'm' and status_board.status[i][j] != final_board.status[i][j]:
                wrong_tiles += 1
    return wrong_tiles


def heuristicTiles(status_board, final_board):
    success = 0
    fail = 0

    while True:
        status_board.hx = countTiles(status_board, final_board)
        print(status_board.hx)
        nodes_list = operators(status_board)
        status_board = findBestStatus(nodes_list)


    return success


def countDistance(status_board, final_board):
    # dictionaries
    status_positions = {}
    goal_positions = {}

    for x1, x2 in zip(range(len(status_board.status)), range(len(final_board.status))):
        for y1, y2 in zip(range(len(status_board.status[x1])), range(len(final_board.status[x2]))):
            if status_board.status[x1][y1] != 'm':
                # status_positions[key] = (tuples)
                status_positions[status_board.status[x1][y1]] = (x1, y1)
            if final_board[x2][y2] != 'm':
                goal_positions[final_board.status[x2][y2]] = (x2, y2)

    distance = 0
    for num, (sx, sy) in status_positions.items():
        gx, gy = goal_positions[num]
        distance += abs(gx - sx) + abs(gy - sy)

    return distance


def heuristicDistance(status_board, final_board):
    success = 0
    fail = 0

    status_board.hx = countDistance(status_board, final_board)
    print(status_board.hx)
    findBestStatus(status_board)

    return success


def chooseHeuristic(status_board, final_board):
    while True:
        heuristic = input('Pick a Heuristic (Enter a number): \n 1. Misplaced Tiles\n 2. Manhattan Distance\n')

        try:
            heuristic = int(heuristic)
            if heuristic == 1:
                heuristicTiles(status_board, final_board)
                break
            elif heuristic == 2:
                heuristicDistance(status_board, final_board)
                break
            else:
                print("Invalid input. Please enter integer 1 or 2. Try again: ")
                continue
        except ValueError:
            print("Invalid input. Please enter integer 1 or 2. Try again: ")
            continue


def showBoard(range_rows, range_cols, board, type_of_board):
    print(f'This is {type_of_board} board:')
    for i in range(range_rows):
        for j in range(range_cols):
            print(f"| {board[i][j]} ", end="")
        print("|")
    print("\n")


def getBoard(range_rows, range_cols, board, type_of_board):
    m_count = 0

    print(f'Enter {type_of_board} 8-puzzle problem (use ''m'' to represent the empty space):')
    for i in range(range_rows):
        get_element = []
        for j in range(range_cols):

            while True:
                user_input = input()

                if user_input == 'm':
                    if m_count == 0:
                        get_element.append(user_input)
                        m_count += 1
                        break
                    else:
                        print("You can only enter 'm' once. Try again and enter an integer: ")
                        continue
                else:
                    try:
                        integer_value = int(user_input)
                        get_element.append(integer_value)
                        break
                    except ValueError:
                        print("Invalid input. Please enter 'm' or an integer. Try again: ")
                        continue

        board.append(get_element)

    showBoard(range_rows, range_cols, board, type_of_board)
    return board


if __name__ == '__main__':
    rows = 3
    cols = 3

    initial_board = []
    goal_board = []

    initial_board = getBoard(rows, cols, initial_board, "initial")
    status_board = Node(initial_board)
    current_parent = status_board
    goal_board = getBoard(rows, cols, goal_board, "goal")
    final_board = Node(goal_board)
    chooseHeuristic(status_board, final_board)
