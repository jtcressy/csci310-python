import sys


def main(line):
    template = "4 {0} 4 {1} 4 {2} 4 = {3}"
    operators = ['*', '+', '-', '//']
    pops = {'*': '*', '+': '+', '-': '-', '//': '/'}
    result = int(line)
    found = False
    for op1 in operators:
        for op2 in operators:
            for op3 in operators:
                if eval("4{}4{}4{}4".format(op1, op2, op3)) == result:
                    return template.format(pops[op1], pops[op2], pops[op3], result)
    return "no solution"


def test():
    assert main('9') == "4 + 4 + 4 / 4 = 9"
    assert main('0') == "4 * 4 - 4 * 4 = 0"
    assert main('7') == "4 + 4 - 4 / 4 = 7"
    assert main('11') == "no solution"
    assert main('24') == "4 * 4 + 4 + 4 = 24"


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    total = int(lines[0])
    for i in range(0, total):
        print(main(lines[i+1]))
