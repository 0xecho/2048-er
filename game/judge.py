from threading import Thread
from multiprocessing import Process
from tempfile import NamedTemporaryFile
from django.conf import settings
import os, json
from time import sleep
from math import log2
import string
import random

def rand_str():
    opt = ""
    for i in range(20):
        opt += random.choice(string.ascii_letters)
    return opt

def judge(submission):
    out_file = NamedTemporaryFile(mode="r+")
    seq_file = NamedTemporaryFile(mode="r+")
    ind_file = NamedTemporaryFile(mode="r+")
    pipe_name = "/tmp/"+rand_str()
    
    os.system(f"bash -c 'mkfifo {pipe_name} && python3 {submission.code_file.path} < {pipe_name} | python3 {settings.BASE_DIR/'game/gen.py'} {submission.seed} {seq_file.name} {ind_file.name} {out_file.name} {pipe_name} > {pipe_name}'")
    print(f"bash -c 'mkfifo {pipe_name} && python3 {submission.code_file.path} < {pipe_name} | python3 {settings.BASE_DIR/'game/gen.py'} {submission.seed} {seq_file.name} {ind_file.name} {out_file.name} {pipe_name} > {pipe_name}'")

    # lst = []
    # with open(out_file.name, "r+") as f:
    #     for line in f.readlines():
    #         lst.append(line.strip())
    lst = json.load(out_file)
    print(lst)

    score = 0
    for row in lst:
        for col in row:
            try:
                score += int(col) * log2(int(col))
            except:
                pass
       
    submission.score = score
    submission.moves_history = open(seq_file.name, "r").read().strip()
    submission.indexes_state = ind_file.read().strip()
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