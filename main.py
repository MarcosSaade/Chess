import pygame
from functions import *


class Main:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.mover = Mover()

        self.w_props, self.b_props = generate_pieces()  # List with name, colour of all pieces
        self.w_pieces, self.b_pieces = [], []  # Lists with Piece objects

        self.w_ids = []  # List with Ids -> (W0, W1, ..., W16)
        self.b_ids = []  # (B0, ..., B16)

    def start(self):
        self.board.generate_board()
        self.board.represent_pieces()

        for i in self.w_props:
            self.w_pieces.append(Piece(i[0], i[1]))

        for i in self.b_props:
            self.b_pieces.append(Piece(i[0], i[1]))

    def update(self):
        self.board.draw()
        self.board.gui_pieces()
        self.mover.check_move()


class Board:
    def __init__(self):
        self.tile_size = WIDTH / 8
        self.tiles = []

        self.w_pawn = pygame.image.load('data/img/wP.png').convert_alpha()
        self.w_rook = pygame.image.load('data/img/wR.png').convert_alpha()
        self.w_knight = pygame.image.load('data/img/wN.png').convert_alpha()
        self.w_bishop = pygame.image.load('data/img/wB.png').convert_alpha()
        self.w_queen = pygame.image.load('data/img/wQ.png').convert_alpha()
        self.w_king = pygame.image.load('data/img/wK.png').convert_alpha()

        self.b_pawn = pygame.image.load('data/img/bP.png').convert_alpha()
        self.b_rook = pygame.image.load('data/img/bR.png').convert_alpha()
        self.b_knight = pygame.image.load('data/img/bN.png').convert_alpha()
        self.b_bishop = pygame.image.load('data/img/bB.png').convert_alpha()
        self.b_queen = pygame.image.load('data/img/bQ.png').convert_alpha()
        self.b_king = pygame.image.load('data/img/bK.png').convert_alpha()

        self.row0 = []
        self.row1 = []
        self.row2 = []
        self.row3 = []
        self.row4 = []
        self.row5 = []
        self.row6 = []
        self.row7 = []

        self.rows = [self.row0, self.row1, self.row2, self.row3, self.row4, self.row5, self.row6, self.row7]

    def generate_board(self):
        for i in range(8):
            for j in range(8):
                self.tiles.append(
                    pygame.rect.Rect(self.tile_size * i, self.tile_size * j, self.tile_size, self.tile_size))

    def draw(self):
        count = 1
        zebra = 1
        for index, i in enumerate(self.tiles):
            if index % 2 == 1:
                if zebra == 1:
                    color = COLOR_1
                else:
                    color = COLOR_2
            else:
                if zebra == 1:
                    color = COLOR_2
                else:
                    color = COLOR_1
            pygame.draw.rect(screen, color, i)
            if count == 8:
                zebra = zebra * -1
                count = 1
            else:
                count += 1

    def represent_pieces(self):
        # Delete past piece representation
        for i in range(8):
            self.rows[i] = []

        # Create new piece representation
        for col in range(8):
            for row in range(8):
                current_row = self.rows[row]
                current_piece = board[row][col]
                if current_piece.__contains__('w'):
                    current_row.append(((0 + (col * WIDTH / 8), 0 + (row * HEIGHT / 8) + 5), current_piece))
                elif current_piece.__contains__('b'):
                    current_row.append(((0 + (col * WIDTH / 8), 0 + (row * HEIGHT / 8) + 5), current_piece))

    def gui_pieces(self):
        # Draw pieces from representation map
        for i in range(8):
            current_row = self.rows[i]  # different from variable above
            for j in range(len(current_row)):
                current_piece = current_row[j][1]
                if current_piece.__contains__('w'):
                    if current_piece.__contains__('P'):
                        screen.blit(self.w_pawn, (current_row[j][0]))
                    elif current_piece.__contains__('R'):
                        screen.blit(self.w_rook, (current_row[j][0]))
                    elif current_piece.__contains__('N'):
                        screen.blit(self.w_knight, (current_row[j][0]))
                    elif current_piece.__contains__('B'):
                        screen.blit(self.w_bishop, (current_row[j][0]))
                    elif current_piece.__contains__('Q'):
                        screen.blit(self.w_queen, (current_row[j][0]))
                    elif current_piece.__contains__('K'):
                        screen.blit(self.w_king, (current_row[j][0]))
                elif current_piece.__contains__('b'):
                    if current_piece.__contains__('P'):
                        screen.blit(self.b_pawn, (current_row[j][0]))
                    elif current_piece.__contains__('R'):
                        screen.blit(self.b_rook, (current_row[j][0]))
                    elif current_piece.__contains__('N'):
                        screen.blit(self.b_knight, (current_row[j][0]))
                    elif current_piece.__contains__('B'):
                        screen.blit(self.b_bishop, (current_row[j][0]))
                    elif current_piece.__contains__('Q'):
                        screen.blit(self.b_queen, (current_row[j][0]))
                    elif current_piece.__contains__('K'):
                        screen.blit(self.b_king, (current_row[j][0]))


class Mover:
    def __init__(self):
        self.start, self.end = -1, -1

        self.turn = 0

    def check_move(self):
        if self.start == -1 or self.end == -1:
            return

        start_x = self.start[1]  # row (down -> up)
        start_y = self.start[0]  # column (left -> right)
        end_x = self.end[1]
        end_y = self.end[0]

        piece = board[start_x][start_y]
        target = board[end_x][end_y]

        if piece.__contains__('P'):
            # TODO en pasant
            can_take = False

            # Take diagonally
            if self.turn == 0:
                t1 = board[start_x - 1][start_y - 1]
                t2 = board[start_x - 1][start_y + 1]
            else:
                t1, t2 = ['  ', '  ']  # Initialize t1 and t2 to prevent bugs on A and H files

                try:
                    t1 = board[start_x + 1][start_y - 1]
                    t2 = board[start_x + 1][start_y + 1]
                except:
                    pass

            if t1 != '  ' or t2 != '  ':
                can_take = True

            # Don't move backwards
            if self.turn == 0:
                if end_x >= start_x:
                    return
            else:
                if end_x <= start_x:
                    return

            # Don't move sideways
            if can_take:
                if end_y not in [start_y - 1, start_y, start_y + 1]:
                    return
            else:
                if start_y != end_y:
                    return

            # Move one space, or two if hasn't moved
            if self.turn == 0:
                if start_x == 6:  # hasn't moved
                    if start_x not in [end_x + 1, end_x + 2]:
                        return
                else:  # has moved
                    if end_x + 1 != start_x:
                        return
            else:
                if start_x == 1:
                    if start_x not in [end_x - 1, end_x - 2]:
                        return
                else:
                    if end_x - 1 != start_x:
                        return

            # Don't move if piece in front
            if can_take:
                front = False  # initialize

                if start_y == end_y and target == '  ':
                    front = True  # it is able to go front

                if front is False:
                    if start_y == end_y:  # if tries go go front and can't, don't
                        return

                    if self.turn == 0:
                        if not target.__contains__('b'):  # w can only eat b, vice versa
                            return
                    else:
                        if not target.count('w'):
                            return
            else:
                if target != '  ':
                    return

        elif piece.__contains__('R'):
            if start_x == end_x:
                axis = 0  # horizontal
            elif start_y == end_y:
                axis = 1  # vertical
            else:
                axis = -1  # invalid

            if axis == 0:
                if start_y < end_y:
                    direction = 'r'
                else:
                    direction = 'l'
            elif axis == 1:
                if start_x > end_x:
                    direction = 'u'
                else:
                    direction = 'd'
            else:
                direction = -1

            # Only straight lines
            if axis == -1:
                return

            # Don't jump pieces
            if straight_obstacles(direction, start_x, start_y, end_x, end_y, target, self.turn):
                return

        elif piece.__contains__('N'):
            if end_y not in [start_y - 2, start_y - 1, start_y + 1, start_y + 2]:
                return

            if end_y == start_y - 2:
                if end_x not in [start_x - 1, start_x + 1]:
                    return
            elif end_y == start_y - 1:
                if end_x not in [start_x - 2, start_x + 2]:
                    return
            if end_y == start_y + 1:
                if end_x not in [start_x - 2, start_x + 2]:
                    return
            elif end_y == start_y + 2:
                if end_x not in [start_x - 1, start_x + 1]:
                    return

            # don't eat own pieces
            if self.turn == 0 and target.__contains__('w'):
                return
            if self.turn == 1 and target.__contains__('b'):
                return

        elif piece.__contains__('B'):
            diff_x = abs(start_x - end_x)
            diff_y = abs(start_y - end_y)

            if diff_x != diff_y:  # Only diagonal movements
                return

            if diff_x == 0:  # Can't move into itself
                return

            #  Up or down
            if end_x < start_x:
                vertical = 0  # upwards
            elif end_x > start_x:
                vertical = 1  # downwards
            else:
                vertical = -1

            # Get direction
            if vertical == 0:
                if start_y < end_y:
                    direction = 'ur'
                else:
                    direction = 'ul'
            elif vertical == 1:
                if start_y < end_y:
                    direction = 'dr'
                else:
                    direction = 'dl'
            else:
                direction = -1

            # Obstacle management
            if diagonal_obstacles(direction, start_x, start_y, self.turn, diff_x):
                return

        elif piece.__contains__('Q'):
            diff_x = abs(start_x - end_x)
            diff_y = abs(start_y - end_y)

            direction = ''  # TODO remove

            if start_x == end_x and start_y == end_y:  # Into itself
                return

            if start_x > end_x:  # up
                if start_y > end_y:
                    direction = 'ul'
                elif start_y < end_y:
                    direction = 'ur'
                else:  # equal
                    direction = 'u'
            if start_x < end_x:  # down
                if start_y > end_y:
                    direction = 'dl'
                elif start_y < end_y:
                    direction = 'dr'
                else:  # equal
                    direction = 'd'
            if start_x == end_x:
                if start_y < end_y:
                    direction = 'r'
                else:
                    direction = 'l'

            # Diagonal movements
            if direction in ['ul', 'ur', 'dl', 'dr']:
                if diff_x != diff_y:
                    return
                if diagonal_obstacles(direction, start_x, start_y, self.turn, diff_x):
                    return
            else:
                if straight_obstacles(direction, start_x, start_y, end_x, end_y, target, self.turn):
                    return

        elif piece.__contains__('K'):
            if end_x not in [start_x - 1, start_x, start_x + 1]:
                return
            if end_y not in [start_y - 1, start_y, start_y + 1]:
                return

            if self.turn == 0 and target.__contains__('w'):
                return
            if self.turn == 1 and target.__contains__('b'):
                return

        self.move()

    def move(self):
        start_x = self.start[1]
        start_y = self.start[0]

        piece = board[start_x][start_y]
        if piece == '  ':
            self.start, self.end = -1, -1
            return

        if self.start == self.end:
            return
        if self.start == -1:
            return
        else:
            if clicked_on(self.start) == self.turn:  # check if he's trying to move his own piece

                if self.start != -1 and self.end != -1:
                    start_x = self.start[1]
                    start_y = self.start[0]
                    end_x = self.end[1]
                    end_y = self.end[0]

                    board[end_x][end_y] = board[start_x][start_y]
                    board[start_x][start_y] = '  '

                    self.start, self.end = -1, -1

                    self.turn = 1 if self.turn == 0 else 0

                    main.board.represent_pieces()


class Piece:
    def __init__(self, name, colour):
        self.colour = colour
        self.name = name

        if colour == 'w':
            self.id = 'W' + str(len(main.w_ids))
            main.w_ids.append(self.id)  # is it necessary to have them in main?
        else:
            self.id = 'B' + str(len(main.b_ids))
            main.b_ids.append(self.id)


class Player:
    def __init__(self):
        pass


def print_board():
    print('-------------------------------------------')
    for i in board:
        print(i)
    print('-------------------------------------------')


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                print_board()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            square = mouse_to_square(mouse[0], mouse[1])

            if main.mover.start == -1:
                main.mover.start = square
            elif main.mover.end == -1:
                main.mover.end = square
            else:
                main.mover.end = -1
                main.mover.start = square


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
main = Main()
main.start()

while True:
    screen.fill((0, 0, 0))
    events()
    clock.tick(FPS)
    main.update()
    pygame.display.update()
