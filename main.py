import queue
import sys
from itertools import count
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


def findSpace(current_node):
    for i in range(len(current_node.status)):
        for j in range(len(current_node.status[i])):
            if current_node.status[i][j] == 'm':
                return i, j


def copyBoard(board):
    return [row[:] for row in board]


def setNode(current_node, operator):
    successor_node = Node(copyBoard(current_node.status), "status")
    successor_node.parent = current_node
    successor_node.steps_gx = current_node.steps_gx + 1
    successor_node.current_operator = operator
    successor_node.previous_operators = current_node.previous_operators.copy()
    successor_node.previous_operators.append(operator)
    successor_node.node_depth = current_node.node_depth + 1

    return successor_node


# https://github.com/boppreh/keyboard/blob/master/README.md
# https://github.com/boppreh/keyboard#keyboardeventname
def operators(current_node):
    space = findSpace(current_node)
    nodes_list = []

    if canMoveLeft(space):
        successor_node = setNode(current_node, "left")
        nodes_list.append(successor_node)
        moveLeft(successor_node, space)

    if canMoveRight(space, current_node):
        successor_node = setNode(current_node, "right")
        nodes_list.append(successor_node)
        moveRight(successor_node, space)

    if canMoveUp(space):
        successor_node = setNode(current_node, "up")
        nodes_list.append(successor_node)
        moveUp(successor_node, space)

    if canMoveDown(space, current_node):
        successor_node = setNode(current_node, "down")
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


def findBestStatus(nodes_list, goal_node, heuristic_type):
    lower_sum = sys.maxsize
    best_node = []

    for node in nodes_list:
        if heuristic_type == "tiles":
            node.hx = countTiles(node, goal_node)
        elif heuristic_type == "manhattan":
            node.hx = countDistance(node, goal_node)
        node.fx = node.steps_gx + node.hx

        if node.fx < lower_sum:
            lower_sum = node.fx
            best_node = [node]
        elif node.fx == lower_sum:
            best_node.append(node)

    return best_node


def countTiles(current_node, goal_node):
    wrong_tiles = 0
    for i in range(len(current_node.status)):
        for j in range(len(current_node.status[i])):
            if current_node.status[i][j] != 'm' and current_node.status[i][j] != goal_node.status[i][j]:
                wrong_tiles += 1
    return wrong_tiles


def heuristic(current_node, goal_node, heuristic_type):
    count_nodes = count()

    if heuristic_type == "tiles":
        current_node.hx = countTiles(current_node, goal_node)
    elif heuristic_type == "manhattan":
        current_node.hx = countDistance(current_node, goal_node)

    current_node.fx = current_node.steps_gx + current_node.hx

    i = 0
    nodes_queue = queue.PriorityQueue()
    nodes_queue.put(((-current_node.steps_gx, next(count_nodes)), current_node))
    # data structure --> hash, index --> value
    existing_boards = set()
    set_node = current_node

    while True:

        if nodes_queue.empty():
            print("\n###############################################################")
            print("### Did not find solution for this problem, queue is empty. ###")
            print("###############################################################\n")
            print(count_nodes)
            showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, set_node.board_type)
            showNodeParam(set_node)
            break

        set_node = nodes_queue.get(block=False)[1]

        if i == 1000000:
            print("\n##############################################################")
            print("### Did not find solution for this problem, too may steps. ###")
            print("##############################################################\n")
            showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, set_node.board_type)
            showNodeParam(set_node)
            break

        if set_node.status == goal_node.status:
            print("\n**********************")
            print("*** Problem solved ***")
            print("**********************\n")
            set_node.board_type = goal_node.board_type
            showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, set_node.board_type)
            showNodeParam(set_node)
            break

        board_tuple = tuple(map(tuple, set_node.status))
        if board_tuple in existing_boards:
            continue

        existing_boards.add(board_tuple)
        nodes_list = operators(set_node)
        possible_nodes = findBestStatus(nodes_list, goal_node, heuristic_type)

        for node in possible_nodes:
            nodes_queue.put(((-node.steps_gx, next(count_nodes)), node))

        showBoard(len(set_node.status), len(set_node.status[0]), set_node.status, set_node.board_type)
        showNodeParam(set_node)
        i += 1


def countDistance(current_node, goal_node):
    # dictionaries
    status_positions = {}
    goal_positions = {}

    for x1, x2 in zip(range(len(current_node.status)), range(len(goal_node.status))):
        for y1, y2 in zip(range(len(current_node.status[x1])), range(len(goal_node.status[x2]))):
            if current_node.status[x1][y1] != 'm':
                # status_positions[key] = (tuples)
                status_positions[current_node.status[x1][y1]] = (x1, y1)
            if goal_node.status[x2][y2] != 'm':
                goal_positions[goal_node.status[x2][y2]] = (x2, y2)

    distance = 0
    for num, (sx, sy) in status_positions.items():
        gx, gy = goal_positions[num]
        distance += abs(gx - sx) + abs(gy - sy)

    return distance


def chooseHeuristic(current_node, goal_node):
    while True:
        pick_heuristic = input('Pick a Heuristic (Enter a number): \n 1. Misplaced Tiles\n 2. Manhattan Distance\n')

        try:
            pick_heuristic = int(pick_heuristic)
            if pick_heuristic == 1:
                heuristic(current_node, goal_node, "tiles")
                break
            elif pick_heuristic == 2:
                heuristic(current_node, goal_node, "manhattan")
                break
            else:
                print("Invalid input. Please enter integer 1 or 2. Try again: ")
                continue
        except ValueError:
            print("Invalid input. Please enter integer 1 or 2. Try again: ")
            continue


# def showSolution(goal_node):
#     stack = []
#     current_node = goal_node
#
#     # Push nodes onto the stack until we reach the root node
#     while current_node:
#         stack.append(current_node)
#         current_node = current_node.parent
#
#     # Pop and print nodes from the stack in reverse order
#     while stack:
#         current_node = stack.pop()
#         showBoard(len(current_node.status), len(current_node.status[0]), current_node.status, current_node.board_type)
#         showNodeParam(current_node)


def showBoard(range_rows, range_cols, board, type_of_board):

    print(f'\nThis is {type_of_board} board:')
    for i in range(range_rows):
        for j in range(range_cols):
            print(f"| {board[i][j]} ", end="")
        print("|")


def showNodeParam(node):
    print(f'Last used operator: {node.current_operator}')
    print(f'Previous operators:')
    for operator in node.previous_operators:
        print(f'- {operator}')
    print(f'----------- Node depth: {node.node_depth}')
    print(f'Heuristic sum: f({node.fx}) = g({node.steps_gx}) + h({node.hx})')


def getNode(range_rows, range_cols, board, type_of_board):
    m_count = 0

    print(f'\nEnter {type_of_board} 8-puzzle problem (use ''m'' to represent the empty space):')
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


def getSize(size):
    while True:
        row_range = input(f'Enter {size}-dimension of m*n-puzzle problem:')

        try:
            if row_range.isdigit():
                return int(row_range)
        except ValueError:
            print("Invalid input. Please enter positive integer. Try again: ")
            continue


def validateBoards(current_board, final_board):

    not_solved_board = {item for row in current_board for item in row}
    solved_board = {item for row in final_board for item in row}
    return not_solved_board == solved_board


if __name__ == '__main__':
    initial_board = []
    goal_board = []

    rows = getSize("m")
    cols = getSize("n")
    initial_board = getNode(rows, cols, initial_board, "initial")
    status_node = Node(initial_board, "initial")
    goal_board = getNode(rows, cols, goal_board, "goal")
    final_node = Node(goal_board, "goal")

    while True:
        valid = validateBoards(initial_board, goal_board)
        if valid:
            chooseHeuristic(status_node, final_node)
            break
        else:
            print("Try again to type goal_board")
            goal_board = getNode(rows, cols, [], "goal")
            final_node = Node(goal_board, "goal")
