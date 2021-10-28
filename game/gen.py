import math , random
import sys

def rotate_right(board):
    tmp = list(zip(*board[::-1]))
    new_board = []
    for row in tmp:
        new_board.append(list(row))
    return new_board

def rotate_left(board):
    for _ in range(3):
        board = rotate_right(board)
    return board

def make_left_move(board):
        new_board = []
        for row in board:
            new_row = []
            non_zero_row = [i for i in row if i]
            while len(non_zero_row)>1:
                a, b = non_zero_row.pop(0),non_zero_row.pop(0)
                if a == b:
                    new_row.append(a+b)
                else:
                    new_row.append(a)
                    non_zero_row = [b]+non_zero_row
            new_row += non_zero_row
            while len(new_row)<4:
                new_row.append(0)
            new_board.append(new_row)
        return new_board

def make_right_move(board):
    temp_board = [i[::-1] for i in board]
    temp_board = [i[::-1] for i in make_left_move(temp_board)]
    return temp_board

def make_up_move(board):
    temp_board = rotate_right(board)
    return rotate_left(make_right_move(temp_board))

def make_down_move(board):
    temp_board = rotate_left(board)
    return rotate_right(make_right_move(temp_board))

def make_random_move(board):
    num = 4 if random.randint(0,9)==9 else 2
    zeroes = []
    for ridx, row in enumerate(board):
        for cidx, col in enumerate(row):
            if col==0:
                zeroes.append([ridx, cidx])
    if not zeroes:
        return board
    random_pos = random.choice(zeroes)
    print([random_pos, num])
    board[random_pos[0]][random_pos[1]] = num
    return board

class Board:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self, board):
        self.board = board

    def score(self):
        score = 0
        for row in self.board:
            for col in row:
                try:
                    score += col * math.log2(col)
                except:
                    pass
        return score
    
    def is_over(self):
        # Has an empty square = Game not over
        for row in self.board:
            for col in row:
                if col==0:
                    return False
        # Has two similar numbers next to each other on one row
        for row in self.board:
            for cidx in range(len(row)-1):
                if row[cidx] == row[cidx+1]:
                    return False
        # Has two similar numbers next to each other on one column
        rotated_board = rotate_right(self.board)
        for row in rotated_board:
            for cidx in range(len(row)-1):
                if row[cidx] == row[cidx+1]:
                    return False
        return True

    def show(self):
        for row in self.board:
            print(*row)

random.seed(sys.argv[1])

moves = [
    make_left_move,
    make_up_move,
    make_right_move,
    make_down_move
]

MOVE_LIMIT = 10_000
move_count = 0

board = Board([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],])
for _ in range(2):
    new_state = make_random_move(board.board)
    board = Board(new_state)
board.show()
print(board.score())

while True:
    move = input()
    try:
        move = int(move)
        if not move in range(0,4):
            raise
    except:
        print("GAMEOVER")
        sys.exit()
    move_count += 1
    
    move_func = moves[move]
    new_state = move_func(board.board)
    new_state = make_random_move(new_state)
    board = Board(new_state)
    
    if board.is_over() or move_count > MOVE_LIMIT:
        print("GAMEOVER")
        sys.exit()
    board.show()
    print(board.score())
