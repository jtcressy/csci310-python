"""
Kattis Problem: https://open.kattis.com/problems/backspace
Accepted Submission: https://open.kattis.com/submissions/2250677
"""


def process(line):
    output = []
    for idx in range(0, len(line)):
        if line[idx] == "<":
            output.pop()
        else:
            output.append(line[idx])
    return ''.join(output)


if __name__ == "__main__":
    print(process(str(input())))
