import sys
import subprocess

game_file = sys.argv[1]
code_file = sys.argv[2]
seed = sys.argv[3]

game_process = subprocess.Popen(['/usr/bin/env', 'python3', game_file, seed], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
code_process = subprocess.Popen(['/usr/bin/env', 'python3', code_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

INDEXES = []
MOVES = []
SCORE = ""

for _ in range(2):
    line = game_process.stdout.readline().strip().decode()
    INDEXES.append(line)

while True:
    row = game_process.stdout.readline().strip().decode()
    if row=="GAMEOVER":
        break
    board = [row] + [game_process.stdout.readline().strip().decode() for _ in range(3)]
    score = game_process.stdout.readline().strip().decode()
    SCORE = score
    try:
        for row in board:
            code_process.stdin.write((row+"\n").encode())
        code_process.stdin.flush()
        move = code_process.stdout.readline().strip().decode()
    except:
        break

    if not move:
        break
    MOVES.append(move)
    game_process.stdin.write((move+"\n").encode())
    game_process.stdin.flush()

    line = game_process.stdout.readline().strip().decode()
    if not line or line == "GAMEOVER":
        break
    INDEXES.append(line)

print({"INDEXES": INDEXES, "MOVES": MOVES, "SCORE": SCORE})