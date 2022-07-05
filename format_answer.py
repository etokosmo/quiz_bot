import re


def format_answer(answer: str) -> str:
    answer = re.sub(r"\(.*\)", "", answer)
    answer = answer.split(".")[0].strip().lower()
    answer = re.sub(r"[,\"']", "", answer)
    return answer
