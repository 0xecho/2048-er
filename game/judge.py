from threading import Thread
from multiprocessing import Process
from tempfile import NamedTemporaryFile
from django.conf import settings
import os
from math import log2

def judge(submission):
    out_file = NamedTemporaryFile(mode="r+")
    os.system(f"bash -c 'python3 {submission.code_file.path} < {out_file.name} | python3 {settings.BASE_DIR/'game/gen.py'} {submission.seed} > {out_file.name}'")

    lst = []
    with open(out_file.name, "r+") as f:
        for line in f.readlines():
            lst.append(line.strip())
    score = 0

    for row in lst[-4:]:
        for col in row.split(" "):
            try:
                score += int(col) * log2(int(col))
            except:
                pass
        
    submission.score = score
    if not lst:
        submission.status = "Runtime Error"

    submission.save()

class Judge(Thread):

    def __init__(self, submission):
        super().__init__()
        self.submission = submission

    def run(self):
        p = Process(target=judge, args=(self.submission,))
        p.start()
        p.join(10)
        if p.is_alive():
            p.terminate()
            self.submission.status = "Time Limit Exceeded"
            self.submission.save()