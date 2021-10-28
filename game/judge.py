# Re write entire judging to utilize celery and proper restrictions
import epicbox

epicbox.configure(profiles=[
    epicbox.Profile("python", "python:3.8.12-alpine")
])
GLOBAL_LIMITS = {"cputime": 60, "memory": 512}


def judge(submission):
    file_name = submission.code_file.name
    file_content = open(file_name, "rb").read()
    file_name = file_name.split("/")[-1]
    if not file_name.endswith(".py"):
        file_name += ".py"
    files = [{"name": file_name, "content": file_content}]
    result = epicbox.run("python", f"python3 {file_name}", files=files, limits=GLOBAL_LIMITS)
    print(result)