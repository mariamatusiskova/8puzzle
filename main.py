import queue
import sys
from node import Node

def swap(successor_node, space, num_pos):
    successor_node.status[space[0]][space[1]], successor_node.status[num_pos[0]][num_pos[1]] = \
        successor_node.status[num_pos[0]][num_pos[1]], successor_node.status[space[0]][space[1]]


def moveLeft(successor_node, space):
    swap(successor_node, space, (space[0], space[1] - 1))


def moveRight(successor_node, space):
    swap(successor_node, space, (space[0], space[1] + 1))


def moveUp(successor_node, space):
    swap(successor_node, space, (space[0] - 1, space[1]))


def moveDown(successor_node, space):
    swap(successor_node, space, (space[0] + 1, space[1]))


def findSpace(status_node):
    space = ()

    for i in range(len(status_node.status)):
        for j in range(len(status_node.status[i])):
            if status_node.status[i][j] == 'm':
                return (i, j)


def copyBoard(board):
   return [row[:] for row in board]


def setNode(status_node, operator):
    successor_board = Node(copyBoard(status_node.status))
    successor_board.parent = status_node
    successor_board.steps_gx = successor_board.parent.steps_gx + 1
    successor_board.current_operator = operator

    return successor_board


# https://github.com/boppreh/keyboard/blob/master/README.md
# https://github.com/boppreh/keyboard#keyboardeventname
def operators(status_node):
    space = findSpace(status_node)
    nodes_list = []

    if canMoveLeft(space):
        successor_node = setNode(status_node, "left")
        nodes_list.append(successor_node)
        moveLeft(successor_node, space)

    if canMoveRight(space, status_node):
        successor_node = setNode(status_node, "right")
        nodes_list.append(successor_node)
        moveRight(successor_node, space)

    if canMoveUp(space):
        successor_node = setNode(status_node, "up")
        nodes_list.append(successor_node)
        moveUp(successor_node, space)

    if canMoveDown(space, successor_node):
        successor_node = setNode(status_node, "down")
        nodes_list.append(successor_node)
        moveDown(successor_node, space)

    return nodes_list


def canMoveLeft(space):
    return space[1] > 0


def canMoveRight(space, node):
    return space[1] < len(node.status[0]) - 1


def canMoveUp(space):
    return space[0] > 0


def canMoveDown(space, node):
    return space[0] < len(node.status) - 1


def findBestStatus(nodes_list):

    lower_sum = sys.maxsize
    best_node = []

    for node in nodes_list:
        node.fx = node.steps_gx + node.hx

        if node.fx < lower_sum:
            lower_sum = node.fx
            best_node = [node]
        elif node.fx == lower_sum:
            best_node.append(node)

    return best_node



def countTiles(status_node, final_node):
    wrong_tiles = 0
    for i in range(len(status_node.status)):
        for j in range(len(status_node.status[i])):
            if status_node.status[i][j] != 'm' and status_node.status[i][j] != final_node.status[i][j]:
                wrong_tiles += 1
    return wrong_tiles


def heuristicTiles(status_node, final_node):
    success = 0
    fail = 0

    status_node.hx = countTiles(status_node, final_node)
    print(status_node.hx)
    status_node.fx = status_node.steps_gx + status_node.hx

    i = 0
    nodes_queue = queue.Queue()
    nodes_queue.put(status_node)

    while True:

        if nodes_queue.empty() or i == 1000000:
            break

        set_node = nodes_queue.get()

        if set_node.status == final_node.status:
            showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, "final")
            break

        nodes_list = operators(set_node)
        possible_nodes = findBestStatus(nodes_list)

        for node in possible_nodes:
            nodes_queue.put(node)

        showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, "status")

        i += 1

    return success


def countDistance(status_node, final_node):
    # dictionaries
    status_positions = {}
    goal_positions = {}

    for x1, x2 in zip(range(len(status_node.status)), range(len(final_node.status))):
        for y1, y2 in zip(range(len(status_node.status[x1])), range(len(final_node.status[x2]))):
            if status_node.status[x1][y1] != 'm':
                # status_positions[key] = (tuples)
                status_positions[status_node.status[x1][y1]] = (x1, y1)
            if final_node[x2][y2] != 'm':
                goal_positions[final_node.status[x2][y2]] = (x2, y2)

    distance = 0
    for num, (sx, sy) in status_positions.items():
        gx, gy = goal_positions[num]
        distance += abs(gx - sx) + abs(gy - sy)

    return distance


def heuristicDistance(status_node, final_node):
    success = 0
    fail = 0

    status_node.hx = countDistance(status_node, final_node)
    print(status_node.hx)
    findBestStatus(status_node)

    return success


def chooseHeuristic(status_node, final_node):
    while True:
        heuristic = input('Pick a Heuristic (Enter a number): \n 1. Misplaced Tiles\n 2. Manhattan Distance\n')

        try:
            heuristic = int(heuristic)
            if heuristic == 1:
                heuristicTiles(status_node, final_node)
                break
            elif heuristic == 2:
                heuristicDistance(status_node, final_node)
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


def getNode(range_rows, range_cols, board, type_of_board):
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

    initial_board = getNode(rows, cols, initial_board, "initial")
    status_node = Node(initial_board)
    current_parent = status_node
    goal_board = getNode(rows, cols, goal_board, "goal")
    final_board = Node(goal_board)
    chooseHeuristic(status_node, final_board)
