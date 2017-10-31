"""
Kattis Problem: https://open.kattis.com/problems/addingwords
Accepted Submission: https://open.kattis.com/submissions/2250896
"""
import sys


class Repl:
    def __init__(self):
        self.reserved_words = {
            "calc": self._calc,
            "def": self._def,
            "clear": self.clear
        }
        self.operators = {
            "+": self._sum,
            "-": self._diff
        }
        self.vars = {}
        self.result = ""

    def clear(self, args):
        self.vars = {}
        self.result = ""

    def _sum(self, a, b):
        return a + b

    def _diff(self, a, b):
        return a - b

    def _calc(self, args):
        expression = ' '.join(args[1:])
        invalid = "{} {}".format(expression, "unknown")
        if args[1] not in self.vars:
            self.result = invalid
            return
        a = self.vars[args[1]]
        i = 2
        while args[i] != '=':
            if args[i+1] not in self.vars:
                self.result = invalid
                return
            b = self.vars[args[i+1]]
            a = self.operators[args[i]](a, b)
            i += 2
        for var in self.vars:
            if self.vars[var] == a:
                self.result = "{} {}".format(expression, var)
                return
        self.result = invalid
        return

    def _def(self, args):
        self.vars[args[1]] = int(args[2])
        self.result = ""

    def process(self, line):
        args = line.split()
        self.reserved_words[args[0]](args)


if __name__ == "__main__":
    repl = Repl()
    for line in sys.stdin.readlines():
        repl.process(line)
        if repl.result != "":
            print(repl.result)
