import math , random

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

class Board:
    """
        A boilerplate 2048 board class with the basic functionalities needed to simulate a 2048 board. 
        You can initialize the class using a 4x4 matrix. 
        Example: 
            >>>board_data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 2], [0, 4, 4, 4]]
            >>>new_board = Board(board_data)
            >>>new_board.score()
            >>>new_board.show()
        
        Input:
            While the game is not over, each state is to be read from standard input. 
            Each state will have 4 lines. Each line will have 4 space separated integers.
            Example: 
                0 0 0 0
                0 0 0 0
                0 0 2 2
                0 4 4 4

            ::hint::
            You can accept the next state like this
                >>> board_data = [
                                    list(map(int, input().split())) for i in range(4)
                    ]
        Output:
            Your output for each round, until the game is over, must be an integer between 0-3. It denotes the next move you want to make.
            Each move is mapped to an integer: 
                0 -> LEFT
                1 -> UP
                2 -> RIGHT
                3 -> DOWN

            >>> print(Board.LEFT) # Make a `Left` move on the borad
    """

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

    def show(self):
        print(*self.board, sep="\n")


# Write your code here

# SAMPLE PLAYERS
# #1: A sample player that always moves (up, down, left)
##############################
# idx = 0
# move_list = [Board.UP, Board.DOWN, Board.LEFT]
# while True:
#     try:
#         board_data = [list(map(int, input().split())) for i in range(4)]
#         print(move_list[idx%4])
#     except:
#         break
#     idx+=1
##############################
# #2: A sample player that always chooses the move with the best score after one move
# while True:
#     try:
#         board_data = [list(map(int, input().split())) for i in range(4)]
#         after_up_move = make_up_move(board_data)
#         after_up_score = Board(after_up_move).score()
#         after_down_move = make_down_move(board_data)
#         after_down_score = Board(after_down_move).score()
#         after_left_move = make_left_move(board_data)
#         after_left_score = Board(after_left_move).score()
#         after_right_move = make_right_move(board_data)
#         after_right_score = Board(after_right_move).score()
#         best = max(
#             [
#                 (after_up_score,Board.UP),
#                 (after_down_score,Board.DOWN),
#                 (after_left_score,Board.LEFT),
#                 (after_right_score,Board.RIGHT),
#             ]
#         )
#         print(best[1])
#     except Exception as e:
#         print(e)
#         break
