from re import sub
import sys
import pexpect

game_file = sys.argv[1]
code_file = sys.argv[2]
seed = sys.argv[3]

game = pexpect.spawn(f"env python3 {game_file} {seed}")
game.delaybeforesend = None
submission = pexpect.spawn(f"env python3 {code_file}")
submission.delaybeforesend = None

score = 0
move_history = []

while True:
    print("Loop", file=sys.stderr)
    first_line = game.readline().strip().decode()
    print("First line:", first_line, file=sys.stderr)
    if not first_line or first_line == "GAMEOVER":
        break
    lines = [first_line] + [game.readline().strip().decode() for _ in range(3)]
    score = game.readline().strip().decode()
    print("SCORE", score, file=sys.stderr)
    print("Lines:", lines, file=sys.stderr)
    for line in lines:
        submission.sendline(" ".join(line))
        submission.flush()
    for _ in range(4):
        submission.readline()
    move = submission.readline().strip().decode()
    move_history.append(move)
    print("Move:", move, file=sys.stderr)
    game.sendline(move)
    game.flush()
    game.readline()

print(score)
print(move_history)