import sys
import json
import random

seed = sys.argv[1]
random.seed(seed)

seq_file_name = sys.argv[2]
ind_file_name = sys.argv[3]

N = 4

KEY_CODE = {'left': 37,
            'up': 38,
            'right': 39,
            'down': 40}
KEY_LEFT = 'left'
KEY_UP = 'up'
KEY_RIGHT = 'right'
KEY_DOWN = 'down'

KEYS = [KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN]

indexes = []

class Board(object):
  def __init__(self):
    self.board = [[None] * N for i in range(N)]
    self.score = 0
    self.over = False

  def rotateLeft(self, grid):
    out = self.emptyGrid()
    for c in range(4):
      for r in range(4):
        out[r][3-c] = grid[c][r]
    return out

  def rotateRight(self, grid):
    out = self.emptyGrid()
    for c in range(4):
      for r in range(4):
        out[3-r][c] = grid[c][r]
    return out

  def emptyGrid(self):
    out = list()
    for x in range(4):
      col = list()
      for y in range(4):
        col.append(None)
      out.append(col)
    return out

  def to_move(self, grid, direction):
    out = self.emptyGrid()

    if direction == KEY_UP:
      rot = 1
    elif direction == KEY_RIGHT:
      rot = 2
    elif direction == KEY_DOWN:
      rot = 3
    else:
      rot = 0

    for i in range(rot):
      grid = self.rotateLeft(grid)

    score = 0
    for r in range(4):
      oc = 0
      ic = 0
      while ic < 4:
        if grid[ic][r] is None:
          ic += 1
          continue
        out[oc][r] = grid[ic][r]
        oc += 1
        ic += 1

      ic = 0
      oc = 0
      while ic < 4:
        if out[ic][r] is None:
          break
        if ic == 3:
          out[oc][r] = out[ic][r]
          oc += 1
          break
        if out[ic][r] == out[ic+1][r]:
          #out[oc][r] *= 2
          out[oc][r] = 2*out[ic][r]
          score += out[oc][r]
          ic += 1
        else:
          out[oc][r] = out[ic][r]
        ic += 1
        oc += 1
      while oc < 4:
        out[oc][r] = None
        oc += 1

    for i in range(rot):
      out = self.rotateRight(out)

    return out, score

  def move(self, direction):
    #print 'move', direction
    next_board, got_score = self.to_move(self.board, direction)
    moved = (next_board != self.board)

    self.board = next_board
    self.score += got_score

    # if moved:
      # if not self.randomTile():
        # self.over = True

  def canMove(self, grid, direction):
    return grid != self.to_move(grid, direction)[0]

  def get_empty_cells(self):
    for i in range(N):
      for j in range(N):
        if self.board[i][j] is None:
          yield i, j

  def randomTile(self):
    cells = list(self.get_empty_cells())
    if not cells:
      indexes.append([-1, -1])
      return False
    #print 'cells', cells


    if random.random() < 0.9:
      v = 2
    else:
      v = 4

    cid = random.choice(cells)
    #print cid
    self.board[cid[0]][cid[1]] = v

    indexes.append([cid[0]+cid[1]*4, v])    

    return True

  def show(self):
    for i in range(N):
      for j in range(N):
        if self.board[j][i]:
          print('%d' % self.board[j][i], sep=" ", end=" ")
        else:
          print('0', end=" ")
      print()

board = Board()
board.randomTile()
board.randomTile()
board.show()
count = 0
opt = ""
for line in sys.stdin:
    ipt = int(line.strip())
    opt += line.strip()
    board.move(KEYS[ipt])
    board.randomTile()
    board.show()
    count += 1
    if count==1000:
        break
f = open(seq_file_name, "w")
f.write(opt)
f.close()
f = open(ind_file_name, "w")
f.write(json.dumps(indexes))
f.close()
