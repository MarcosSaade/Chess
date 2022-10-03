from settings import *
import math


def generate_pieces():
    w_pieces = []
    b_pieces = []

    for i in range(8):
        w_pieces.append(('P', 'w'))
        b_pieces.append(('P', 'b'))

    w_pieces.append(('R', 'w'))
    w_pieces.append(('R', 'w'))
    w_pieces.append(('N', 'w'))
    w_pieces.append(('N', 'w'))
    w_pieces.append(('B', 'w'))
    w_pieces.append(('B', 'w'))
    w_pieces.append(('K', 'w'))
    w_pieces.append(('Q', 'w'))

    b_pieces.append(('R', 'b'))
    b_pieces.append(('R', 'b'))
    b_pieces.append(('N', 'b'))
    b_pieces.append(('N', 'b'))
    b_pieces.append(('B', 'b'))
    b_pieces.append(('B', 'b'))
    b_pieces.append(('Q', 'b'))
    b_pieces.append(('K', 'b'))

    return w_pieces, b_pieces


def mouse_to_square(mX, mY):
    sX = math.floor(mX / square_width)
    sY = math.floor(mY / square_width)

    return sX, sY


def clicked_on(square):
    x = square[1]
    y = square[0]

    piece = board[x][y]

    if piece.__contains__('w'):
        return 0
    elif piece.__contains__('b'):
        return 1
    else:
        return -1


def straight_obstacles(direction, start_x, start_y, end_x, end_y, target, turn):
    # Returns 1 for can't move, 0 for can move

    obstacle = -1

    # right
    if direction == 'r':
        available = 7 - start_y  # How many spaces in front
        distance = end_y - start_y  # How many spaces tries to travel
        for i in range(available):
            i = i + 1  # not zero
            if board[start_x][start_y + i] != '  ':
                obstacle = i  # i means how many movements until it touches an obstacle
                break
            else:
                obstacle = 7  # No obstacles on row

        #  To blank space
        if target == '  ':
            if distance > obstacle:
                return 1

        # Can't eat piece behind other piece
        if turn == 0:
            if distance > obstacle and target.__contains__('b'):
                return 1
        else:  # turn == 1
            if distance > obstacle and target.__contains__('w'):
                return 1

        # To existing piece
        if turn == 0:
            if distance >= obstacle and not target.__contains__('b'):
                return 1
        else:
            if distance >= obstacle and not target.__contains__('w'):
                return 1

    # left
    elif direction == 'l':
        available = start_y
        distance = start_y - end_y
        for i in range(available):
            i = i + 1
            if board[start_x][start_y - i] != '  ':
                obstacle = i
                break
            else:
                obstacle = 7

        if target == '  ':
            if distance > obstacle:
                return 1

        if turn == 0:
            if distance > obstacle and target.__contains__('b'):
                return 1
        else:
            if distance > obstacle and target.__contains__('w'):
                return 1

        if turn == 0:
            if distance >= obstacle and not target.__contains__('b'):
                return 1
        else:
            if distance >= obstacle and not target.__contains__('w'):
                return 1

    # up
    elif direction == 'u':
        available = start_x
        distance = start_x - end_x
        for i in range(available):
            i = i + 1
            if board[start_x - i][start_y] != '  ':
                obstacle = i
                break
            else:
                obstacle = 7

        if target == '  ':
            if distance > obstacle:
                return 1

        if turn == 0:
            if distance > obstacle and target.__contains__('b'):
                return 1
        else:
            if distance > obstacle and target.__contains__('w'):
                return 1

        if turn == 0:
            if distance >= obstacle and not target.__contains__('b'):
                return 1
        else:
            if distance >= obstacle and not target.__contains__('w'):
                return 1

    # down
    elif direction == 'd':
        available = (7 - start_x)
        distance = end_x - start_x
        for i in range(available):
            i = i + 1
            if board[start_x + i][start_y] != '  ':
                obstacle = i
                break
            else:
                obstacle = 7

        if target == '  ':
            if distance > obstacle:
                return 1

        if turn == 0:
            if distance > obstacle and target.__contains__('b'):
                return 1
        else:
            if distance > obstacle and target.__contains__('w'):
                return 1

        if turn == 0:
            if distance >= obstacle and not target.__contains__('b'):
                return 1
        else:
            if distance >= obstacle and not target.__contains__('w'):
                return 1

        return 0


def diagonal_obstacles(direction, start_x, start_y, turn, diff_x):
    obstacle = 8

    if direction == 'ur':
        for i in range(7):
            i = i + 1  # Start at 1, not 0

            target = (start_x - i, start_y + i)  # check diagonally for obstacles

            if target[1] < 8:
                current_square = board[target[0]][target[1]]

            try:
                if current_square != '  ':
                    obstacle = i
                    break
            except:
                pass

    elif direction == 'ul':
        for i in range(7):
            i = i + 1

            target = (start_x - i, start_y - i)

            if target[1] < 8:
                current_square = board[target[0]][target[1]]

            try:
                if current_square != '  ':
                    obstacle = i
                    break
            except:
                pass

    elif direction == 'dr':
        for i in range(7):
            i = i + 1

            target = (start_x + i, start_y + i)

            if target[1] < 8:
                current_square = board[target[0]][target[1]]

            try:
                if current_square != '  ':
                    obstacle = i
                    break
            except:
                pass

    elif direction == 'dl':
        for i in range(7):
            i = i + 1

            target = (start_x + i, start_y - i)

            if target[1] < 8:
                current_square = board[target[0]][target[1]]

            try:
                if current_square != '  ':
                    obstacle = i
                    break
            except:
                pass

    if turn == 0 and current_square.__contains__('w'):
        obstacle = obstacle - 1
    elif turn == 1 and current_square.__contains__('b'):
        obstacle = obstacle - 1

    if diff_x > obstacle:
        return 1  # can't move
    else:
        return 0  # can move
