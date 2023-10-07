from node import Node


def findBestStatus(status_board):
    pass


def countTiles(status_board, goal_board):
    wrong_tiles = 0
    for i in range(len(status_board.status)):
        for j in range(len(status_board.status[i])):
            if status_board.status[i][j] != 'm' and status_board.status[i][j] != goal_board[i][j]:
                wrong_tiles += 1
    return wrong_tiles


def heuristicTiles(status_board, goal_board):
    success = 0
    fail = 0

    status_board.hx = countTiles(status_board, goal_board)
    print(status_board.hx)
    findBestStatus(status_board)

    return success


def countDistance(status_board, goal_board):

    # dictionaries
    status_positions = {}
    goal_positions = {}

    for x1, x2 in zip(range(len(status_board.status)), range(len(goal_board))):
        for y1, y2 in zip(range(len(status_board.status[x1])), range(len(goal_board[x2]))):
            if status_board.status[x1][y1] != 'm':
                # status_positions[key] = (tuples)
                status_positions[status_board.status[x1][y1]] = (x1, y1)
            if goal_board[x2][y2] != 'm':
                goal_positions[goal_board[x2][y2]] = (x2, y2)

    distance = 0
    for num, (sx, sy) in status_positions.items():
        gx, gy = goal_positions[num]
        distance += abs(gx - sx) + abs(gy - sy)

    return distance


def heuristicDistance(status_board, goal_board):
    success = 0
    fail = 0

    status_board.hx = countDistance(status_board, goal_board)
    print(status_board.hx)
    findBestStatus(status_board)

    return success


def chooseHeuristic(status_board, goal_board):

    while True:
        heuristic = input('Pick a Heuristic (Enter a number): \n 1. Misplaced Tiles\n 2. Manhattan Distance\n')

        try:
            heuristic = int(heuristic)
            if heuristic == 1:
                heuristicTiles(status_board, goal_board)
                break
            elif heuristic == 2:
                heuristicDistance(status_board, goal_board)
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
    goal_board = getBoard(rows, cols, goal_board, "goal")
    chooseHeuristic(status_board, goal_board)
