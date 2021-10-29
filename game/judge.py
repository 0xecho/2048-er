from re import sub
import epicbox
import threading
from django.conf import settings

epicbox.configure(profiles=[
    epicbox.Profile("python", "0xecho/python3.8.12:latest")
])
GLOBAL_LIMITS = {"cputime": 60, "memory": 512}


def judge(submission):
    t = threading.Thread(target=judge_worker, args=(submission,))
    t.start()

def judge_worker(submission):
    file_name = submission.code_file.name
    file_content = open(file_name, "rb").read()
    file_name = file_name.split("/")[-1]
    if not file_name.endswith(".py"):
        file_name += ".py"
    files = [
        {"name": file_name, "content": file_content},
        {"name": "runner.py", "content": open(settings.RUNNER_FILE_PATH, "rb").read()},
        {"name": "gen.py", "content": open(settings.GAME_FILE_PATH, "rb").read()},
    ]
    result = epicbox.run("python", f"python3 runner.py gen.py {file_name} {submission.seed}", files=files, limits=GLOBAL_LIMITS)
    submission.errors = str(result)
    submission.save()
    output = result.get("stdout").decode()
    output = eval(output)
    moves = output.get("MOVES")
    indexes = output.get("INDEXES")
    score = output.get("SCORE")
    submission.moves_history = ",".join(moves)
    submission.indexes_state = indexes
    submission.score = float(score.strip())
    submission.save()